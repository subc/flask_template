# -*- coding: utf-8 -*-
from module.scraping.search import SearchManager
from module.site.page import Keyword, Page
from module.site.site import Site


for i in range(1, 10):
    print(Keyword.get(i))
for i in range(1, 10):
    print(Keyword.get(i))

page = Page.get(1)
print(page.keywords)
print(page.keywords)
print(page.keywords)
print(page.keywords)

print(page.tile_label)
