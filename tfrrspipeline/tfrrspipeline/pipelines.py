# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html and
# https://www.youtube.com/watch?v=6VFMGthBD58

# See more info here: http://scrapingauthority.com/scrapy-database-pipeline/
import mysql.connector
from scrapy.exceptions import NotConfigured

class TFRRSpipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(db=self.db,
                               user=self.user, passwd=self.passwd,
                               host=self.host,
                               charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""DROP TABLE IF EXISTS tfrrstitle""")
        self.cursor.execute("""CREATE TABLE tfrrstitle (
                            title text
                            )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.cursor.execute("""INSERT INTO tfrrstitle (title) VALUES (%s)""",
                            (
                                item.get('title')
                            ))
        self.conn.commit()
#
# class athletepipeline(object):
#
#     def __init__(self, db, user, passwd, host):
#         self.db = db
#         self.user = user
#         self.passwd = passwd
#         self.host = host
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         db_settings = crawler.settings.getdict("DB_SETTINGS")
#         if not db_settings:
#             raise NotConfigured
#         db = db_settings['db']
#         user = db_settings['user']
#         passwd = db_settings['passwd']
#         host = db_settings['host']
#         return cls(db, user, passwd, host)
#
#     def open_spider(self, spider):
#         self.conn = mysql.connector.connect(db=self.db,
#                                user=self.user, passwd=self.passwd,
#                                host=self.host,
#                                charset='utf8', use_unicode=True)
#         self.cursor = self.conn.cursor()
#         self.cursor.execute("""DROP TABLE IF EXISTS athletes""")
#         self.cursor.execute("""CREATE TABLE athletes (
#                             Season text
#                             )""")
#
#     def process_item(self, item, spider):
#         self.store_db(item)
#         return item
#
#     def store_db(self, item):
#         self.cursor.execute("""INSERT INTO athletes (Season) VALUES (%s)""",
#                             (
#                                 item.get('Season')
#                             ))
#         self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
