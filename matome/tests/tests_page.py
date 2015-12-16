# -*- coding: utf-8 -*-
import random

from module.site.page import Page, Keyword


def tests_page_models():
    # # insert
    # page = Page(site_id=1,
    #             dat_id=12345,
    #             page="agraeg43g34qhg43qh43qh34")
    # page2 = Page(site_id=1,
    #              dat_id=112345,
    #              page="agraeg43g34qhg43qh43qh34")
    #
    # Page.bulk_insert([page, page2])
    #
    # # update
    # page2.dat_id = 22222
    # page2.save()

    all_pages = Page.objects().all()
    for page in all_pages:
        _id = page.site.get_background_image_id(page.id)
        assert 1 <= _id <= 5
        print(_id)
    raise


def tests_keyword():
    site_id = 1
    keywords = ['シタちゃん', 'メタガ']
    for x in range(3):
        result = Keyword.register(site_id, keywords)
        assert type(random.choice(result) == Keyword)

#
# # select
# book1 = Book.get(1)
# books = Book.objects().filter(Book.price==2160).all()
#
# # insert
# book_rye = Book(title="The catcher in the rye",
#                 price=1000,
#                 publish="J. D. Salinger",
#                 published="")
# book_rye = Book.insert(book_rye)
# print(book_rye.id)
#
# # update
# book_rye.price = 1200
# book_rye.save()
#
# # delete
# book_rye.delete()
