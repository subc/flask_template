# -*- coding: utf-8 -*-
import os
from subprocess import PIPE, Popen
from PIL import Image
"""
Python 2系で動作

image converter png to jpg

export FLASK_ROOT=/Users/xxxx/pxxxx/maxxxx
でmanage.pyが存在するディレクトリを登録しておく
"""


def main():
    _base = os.environ['FLASK_ROOT']
    PATH = '{}/static/img/site'.format(_base)

    # get_convert_list
    p = cmdline('find {}|grep .png'.format(PATH))
    png_list = [line.decode("utf-8").replace('\n', '') for line in p.stdout.readlines()]
    print(png_list)

    # start convert
    for image_path in png_list:
        convert_png_to_jpg(image_path)


def convert_png_to_jpg(image_path, aa_enable=True):
    """
    png画像をjpgに変換して保存する
    :param image_path: str
    :param aa_enable: bool
    """
    output_path = image_path.replace('.png', '.jpg')
    print(output_path)

    # 画像をreadonlyで開く
    img = Image.open(image_path, 'r')
    # 画像ピクセルを取得
    x, y = img.size[0], img.size[1]
    resize_img = img
    if aa_enable:
        # アンチエイリアスありで縮小
        resize_img.thumbnail((x, y), Image.ANTIALIAS)
    else:
        # アンチエイリアスなしで縮小
        resize_img = resize_img.resize((x, y))

    # リサイズ後の画像を保存
    resize_img.save(output_path, 'jpeg', quality=90)
    print("PNG to JPG!:{}[{}x{}]".format(image_path, x, y))


def cmdline(command):
    """
    コマンドを実行する。shell=Trueの場合シェル経由で実行する。
    :param command: str
    :return: Popen
    """
    return Popen(
        args=command,
        stdout=PIPE,
        stderr=PIPE,
        shell=True
    )


main()
