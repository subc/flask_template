# -*- coding: utf-8 -*-
from collections import defaultdict

import requests
from werkzeug.utils import cached_property
from janome.tokenizer import Tokenizer
import re
from bs4 import BeautifulSoup

from module.scraping.storage import SearchStorage
from module.site.page import Page, PageType, Keyword


def token_is_sub(token):
    """
    名詞、形容詞以外ならTrue
    """
    if "動詞" in token.part_of_speech:
        return True

    if "助" in token.part_of_speech:
        return True

    if "記号" in token.part_of_speech:
        return True

    if "数" in token.part_of_speech:
        return True

    if "サ変接続" in token.part_of_speech:
        return True

    if re.match(r'[a-zA-Z0-9]', token.surface):
        return True
    return False


def final_filter(prev_token, token):
    """
    最終的に登録するかを判定
    """
    if not prev_token:
        return False

    s = prev_token.surface + token.surface
    if len(s) <= 2:
        return False

    if "スレ" in s:
        return False

    if re.match(r'[ぁ-ん]', s):
        return False

    if re.match(r'[0-9]', token.surface):
        return False

    if len(token.surface) == 1 and re.match(r'[ぁ-ん]', token.surface):
        return False

    return True


def main(subject):
    # 読み込み
    posts = {}
    for posted in dat_reader(subject.dat_url):
        posts[posted.num] = posted

    # 読み込み後のパースとエラー排除とレスによる重み付け
    posts = analyze_post(posts)

    # キーワード解析
    r_indexes = analyze_keyword(posts)

    # postsにキーワード解析内容を反映したあと、keywordデータをDBに一括登録
    insert_keyword(posts, r_indexes, subject.site.id)

    # 評価高い投稿を出力
    pages = []
    for key in posts:
        output = PageRepository(_type=PageType.POST_RANK.value)
        if posts[key].priority > 300:
            # 評価の高い投稿を出力
            print("++++++++++++++++++++")
            print(posts[key].priority)
            print("++++++++++++++++++++")
            posts[key].printer(posts=posts, output=output)
            # DB出力用に記録
            pages.append(output)

    # キーワード評価が高い投稿を出力
    for r_index in r_indexes:
        pages.append(printer_res(r_index, posts))

    # dbに記録
    keyword_record_dict = {r_index.keyword: r_index.keyword_record for r_index in r_indexes}
    Page.bulk_insert([page.output_for_page(subject, keyword_record_dict) for page in pages if page.is_enable])


def analyze_post(posts):
    """
    Postedのセルフチェックと投稿による重み付けを行う
    :param posts: dict{int: Posted}
    :return: dict{int: Posted}
    """
    _r = {}
    for key in posts:
        try:
            posts[key].self_check(posts)
        except:
            pass
        _r[key] = posts[key]
    return _r


class KeywordReverseIndex(object):
    """
    キーワードから文中での出現数と
    出現する投稿を逆索引
    """
    def __init__(self, keyword, count, posts):
        """
        :param keyword: str
        :param count: int
        :param posts: list(Posted)
        :return:
        """
        self.keyword = keyword
        self.count = count
        self.posts = posts
        self.keyword_record = None

    @property
    def is_enable(self):
        """
        出現数が一定以上のキーワードのみ有効
        :return: bool
        """
        return 4 <= self.count

    def insert_keyword_info(self):
        """
        キーワード情報を投稿毎に付与
        """
        for post in self.posts:
            post.priority_from_keyword(self.keyword, self.count)

    def extend_keyword_record(self, record):
        """
        :param record: Keyword
        """
        self.keyword_record = record


def analyze_keyword(posts):
    """
    投稿を形態素解析して頻出ワードで重み付けして
    キーワードから出現数と投稿の逆索引を生成する。
    :param posts: dict{int: Posted}
    :rtype: list(KeywordReverseIndex)
    """
    t = Tokenizer()
    tfidf2 = defaultdict(int)
    tfidf2_post = defaultdict(list)

    # 単語毎の重み付け
    for key in posts:
        post = posts[key]
        for message in post.parse_post_message:
            # Aタグ排除
            soup = BeautifulSoup(message, "lxml")

            # janome
            _prev_token = None
            try:
                for token in t.tokenize(soup.text):
                    # tokenが助詞なら相手しない
                    if final_filter(_prev_token, token):
                        tfidf2[_prev_token.surface + token.surface] += 1
                        if post not in tfidf2_post[_prev_token.surface + token.surface]:
                            tfidf2_post[_prev_token.surface + token.surface] += [post]

                    _prev_token = token

                    # tokenが助詞ならtfidf2の先頭文字から除外
                    if token_is_sub(token):
                        _prev_token = None
            except:
                pass

    # 逆索引の生成
    r_indexes = []
    for key in tfidf2:
        _index = KeywordReverseIndex(key, tfidf2[key], tfidf2_post[key])

        # 出現数が一定以上のキーワードのみindexを生成する
        if _index.is_enable:
            r_indexes.append(_index)
    return r_indexes


def insert_keyword(posts, r_indexes, site_id):
    """
    キーワード情報を投稿に付与
    keywordデータをDBに一括登録
    :param posts: dict{int: Posted}
    :param r_indexes: list(KeywordReverseIndex)
    :param site_id: int
    :rtype : list(Keyword)
    """
    # キーワード情報を投稿に付与
    keywords = []
    for r_index in r_indexes:
        r_index.insert_keyword_info()
        keywords.append(r_index.keyword)

    # DBに一括登録
    keyword_records = Keyword.register(site_id, keywords)

    # r_indexにkeyword_idを登録
    keyword_records_dict = {record.keyword: record for record in keyword_records}
    for r_index in r_indexes:
        record = keyword_records_dict[r_index.keyword]
        r_index.extend_keyword_record(record)


def dat_reader(url):
    """
    HTTPアクセスしてパースして投稿毎に返却するジェネレータ
    :param url: str
    :rtype : list(Posted)
    """
    response = requests.get(url)
    assert (response.status_code == 200), response.text

    # parse
    data = list(response.text.split('\n'))

    for i, line in enumerate(data):
        if 20 < i < len(data) - 5:
            yield Posted(i + 1, line)


def printer_res(r_index, all_posts):
    """
    レス数が多いときは数を減らしてprint
    目安は7

    :param r_index: KeywordReverseIndex
    :param all_posts: dict{int: Posted}
    :rtype : PageRepository
    """
    posts = r_index.posts

    # priorityがマイナスは対象外
    posts = [p for p in posts if p.priority >= 0]
    # 子供は除外
    posts = [p for p in posts if not p.i_am_child]

    limit = 7
    count = len(posts)
    if count >= limit:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(["{}:{}".format(p.num, p.priority) for p in posts])
        _posts = roulette(posts, limit)
        print(["{}:{}".format(p.num, p.priority) for p in _posts])
    else:
        _posts = posts

    # printer
    _posts = sorted(_posts, key=lambda x: x.num)
    _printed = []
    output = PageRepository(_type=PageType.KEYWORD_RANK.value)
    for post in _posts:
        _printed = post.printer(posts=all_posts, printed=_printed, output=output)
    output.printer()
    return output


def roulette(posts, limit):
    """
    priorityによるルーレット選択
    """
    if len(posts) <= limit:
        return posts
    posts = sorted(posts, key=lambda x: x.priority, reverse=True)
    return posts[:limit]


class PageRepository(object):
    def __init__(self, _type):
        self.output = []
        self.counter = 0
        self._matome_type = _type

    @property
    def count(self):
        return self.counter

    @property
    def is_enable(self):
        """
        DB出力するならTrue
        :return: bool
        """
        return self.count > 4

    @property
    def matome_type(self):
        """
        1 .. priority
        2 .. keyword
        :return:
        """
        return self._matome_type

    @property
    def keywords(self):
        r = {}
        for p in self.output:
            for _keyword in p.keywords:
                r[_keyword] = 1
        return list(r.keys())

    def get_keyword_record_ids(self, keyword_record_dict):
        """
        Keywordのidを返却
        :param keyword_record_dict: dict{int: Keyword}
        :return: list(int)
        """
        r = []
        for keyword in self.keywords:
            r.append(keyword_record_dict[keyword])
        return r

    def output_for_page(self, subject, keyword_record_dict):
        """
        DB出力用のPageクラスを出力
        :param subject: Subject
        :param keyword_record_dict: dict{int: Keyword}
        :rtype : Page
        """
        s = ''.join([post.generate_post_message_for_db(prefix_enable=True) for post in self.output])
        keyword_record_ids = [keyword_record.id for keyword_record
                              in self.get_keyword_record_ids(keyword_record_dict)]
        return Page(site_id=subject.site.id,
                    dat_id=subject.dat_id,
                    page=s,
                    page_top=self.output[0].generate_post_message_for_db(),
                    type=self.matome_type,
                    _keywords=','.join([str(_id) for _id in keyword_record_ids]),
                    )

    def _count_up(self):
        self.counter += 1

    def extend(self, p):
        self.output.append(p)
        self._count_up()

    def printer(self):
        if self.count > 4:
            l = [str(p.num) for p in self.output]
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            print('output【{}】:'.format(self.count) + ','.join(l))
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


class Posted(object):
    def __init__(self, num, line):
        self.num = num
        self.line = line
        self.priority = 0
        self.child = []
        self.i_am_child = None
        self.keywords = []

    def __repr__(self):
        return self.parse_post_message[0]

    @property
    def is_enable(self):
        """
        出力する価値がある投稿ならTrue
        :return: bool
        """
        return self.priority >= 0

    @cached_property
    def splited(self):
        return self.line.split('<>')

    @property
    def post_message(self):
        return self.splited[3]

    @cached_property
    def parse_post_message(self):
        return self.post_message.split('<br>')

    @cached_property
    def parse_bs4(self):
        """
        行毎のBeautifulSoupの解析結果
        :rtype : list of BeautifulSoup
        """
        return [BeautifulSoup(m, "lxml") for m in self.parse_post_message]

    @cached_property
    def post_message_for_output(self):
        """
        ポストメッセージからAタグ除外
        """
        r = []
        for soup in self.parse_bs4:
            s = soup.text
            if soup.a:
                for _a in soup.a:
                    s = s.replace(str(_a), "")
            r.append(s)
        return r

    @property
    def count_link(self):
        return sum([len(soup.a) for soup in self.parse_bs4 if soup.a])

    @cached_property
    def res(self):
        """
        >> 1 なら [1]
        >> 234, 561なら [234, 561]
        """
        r = []
        for t in [soup.a.text for soup in self.parse_bs4 if soup.a]:
            res_base = t.replace(">>", "")
            try:
                res = int(res_base)
                if 10 < res < 1000:
                    r.append(res)
            except:
                pass
        return r

    def generate_post_message_for_db(self, prefix_enable=False):
        prefix = ''
        if prefix_enable:
            prefix = '{}<br/>'.format(str(self.num))
        return prefix + ''.join([_s for _s in self.post_message_for_output])

    def set_cheap(self):
        """
        品質が悪い投稿
        """
        self.priority = -10000

    def printer(self, depth=0, posts=None, printed=[], output=None):
        # print済みでなければprintする
        if self.num not in printed and self.is_enable:
            printed.append(self.num)
            if output:
                output.extend(self)
            prefix = "".join(['--' for x in range(depth)])
            print("{}◆◆ {}:{}".format(prefix, str(self.num), str(self.priority)))
            for x in self.post_message_for_output:
                if len(x) > 1:
                    print(prefix, x)

        # 子レスをprint
        if posts:
            printed = [posts[child_res].printer(depth=depth + 1,
                                                posts=posts,
                                                printed=printed,
                                                output=output)
                       for child_res in self.child if posts[child_res].priority >= 0]
        return printed

    def res_from(self, child_res):
        """
        特定投稿からのres
        """
        # 自己評価を上げる
        self.priority += 100

        # 子レスを記録
        self.set_child(child_res)

    def priority_from_keyword(self, keyword, count):
        """
        keywordによるpriorityアップ
        :param keyword: str
        :param count: int
        """
        self.priority += count
        self.keywords.append(keyword)

    def set_child(self, child_res):
        if self.num == child_res:
            return
        self.child.append(child_res)

    def set_i_am_child(self):
        self.i_am_child = True

    def self_check(self, r):
        """
        自己診断する
        """
        # NGワード
        # レス数の検知
        if self.count_link > 1:
            self.set_cheap()
            return

        # 未来に向けたレス
        for res_num in self.res:
            if self.num <= res_num:
                self.set_cheap()
            else:
                # レスによる重み付け
                if res_num in r:
                    parent = r[res_num]
                    parent.res_from(self.num)
                    self.set_i_am_child()
                else:
                    print("NOT FOUND ERROR:{}".format(res_num))

        # 画像かURL入っていたら除外
        for x in self.post_message_for_output:
            if '://' in x:
                self.set_cheap()

        # postedに触っておく
        self.post_message


class MatomeMixin(object):
    @classmethod
    def matome(cls, subject, force=None):
        """
        :param subject: Subject
        :param force: bool
        """
        # redis問い合わせしてまとめるかチェック
        storage = SearchStorage(subject.site.title)

        if not storage.get_dat(subject.dat) or force:
            # まとめる
            main(subject)

            # redisに記録
            storage.set_dat(subject.dat)

        else:
            print('Already Matometa!:{}'.format(str(subject)))
