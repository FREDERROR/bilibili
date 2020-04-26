# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

class BilibiliPipeline(object):
    """
        连接数据库
    """
    collection_name = 'Video_Info'
    def __init__(self,mongo_uri,mongo_db,mongo_port):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db
        self.mongo_port=mongo_port
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'items'),
            mongo_port = crawler.settings.get('MONGO_PORT')
        )
    def open_spider(self,spider):
        #链接数据库
        self.client = pymongo.MongoClient(self.mongo_uri,self.mongo_port) #获得客户端句柄
        self.db =self.client[self.mongo_db] #获得数据库句柄

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

