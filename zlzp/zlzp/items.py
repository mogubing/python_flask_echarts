# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class ZlzpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
# 继承于scrapy.Item
class ZwItem(scrapy.Item):
    zwmc=scrapy.Field()
    gsmc=scrapy.Field()
    zwyx=scrapy.Field()
    zwyx_low = scrapy.Field()
    zwyx_high = scrapy.Field()
    gsdd=scrapy.Field()
    fbsj=scrapy.Field()
    href=scrapy.Field()


# class teacherItem(scrapy.Item):
#     id=scrapy.Field()
#     name=scrapy.Field()
# class courseItem(teacherItem.Item):
#     name=scrapy.Field()

