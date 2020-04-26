# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class VideoItem(scrapy.Item):
    aid = scrapy.Field()
    up_name = scrapy.Field()
    title = scrapy.Field()
    view = scrapy.Field()
    danmaku = scrapy.Field()
    reply = scrapy.Field()
    favorite = scrapy.Field()
    coin = scrapy.Field()
    share = scrapy.Field()
    like = scrapy.Field()
    now_rank = scrapy.Field()
    his_rank = scrapy.Field()


