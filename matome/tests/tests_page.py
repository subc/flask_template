# -*- coding: utf-8 -*-
from module.site.page import Page


def tests_page_models():
    # insert
    page = Page(site_id=1,
                dat_id=12345,
                page="agraeg43g34qhg43qh43qh34")
    page2 = Page(site_id=1,
                 dat_id=112345,
                 page="agraeg43g34qhg43qh43qh34")

    Page.bulk_insert([page, page2])

    # update
    page2.dat_id = 22222
    page2.save()

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
