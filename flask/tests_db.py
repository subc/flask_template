# -*- coding: utf-8 -*-
from module.book import Book
from utils.db import get_db_session

# select
book1 = Book.get(1)
books = Book.objects().filter(Book.price==2160).all()

# insert
book_rye = Book(title="The catcher in the rye",
                price=1000,
                publish="J. D. Salinger",
                published="")
book_rye = Book.insert(book_rye)
print(book_rye.id)

# update
book_rye.price = 1200
book_rye.save()

# delete
book_rye.delete()


# select
print(Book.get(1))

book = get_db_session().query(Book).filter().all()
print(book)
book = get_db_session().query(Book).filter(Book.price == 122222).all()
print(book)

book = Book.objects().filter(Book.price == 122222).all()
print(book)
print(Book.objects().filter(Book.id == 1, Book.price != 1).all())

# insert
book = Book(title="",
            price=123,
            publish="",
            published="")
obj = Book.insert(book)
print(obj.id)

# bulk insert
book1 = Book(title="",
             price=11111,
             publish="",
             published="")
book2 = Book(title="",
             price=2222,
             publish="",
             published="")
objs = Book.bulk_insert([book1, book2])
print([r.id for r in objs])

# delete
obj.delete()

# update
book1.price = 56789
book1.save()



print("finish")
