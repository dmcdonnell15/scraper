# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#See more info here: http://scrapingauthority.com/scrapy-database-pipeline/
import mysql.connector
from scrapy.exceptions import NotConfigured

# class TFRRSpipeline(object):
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
#         self.cursor.execute("""DROP TABLE IF EXISTS tfrrs""")
#         self.cursor.execute("""CREATE TABLE tfrrs (
#                             AthleteName text,
#                             Team text,
#                             Location text,
#                             EventDate text,
#                             Event text,
#                             Performance text,
#                             Place text
#                             )""")
#
#     #def create_table(self):
#     # self.cursor.execute("""DROP TABLE IF EXISTS tfrrs""")
#     # self.cursor.execute("""CREATE TABLE tfrrs (
#     #                     AthleteName text,
#     #                     Grade text,
#     #                     Team text,
#     #                     Location text,
#     #                     EventDate text,
#     #                     Event text,
#     #                     Performance text,
#     #                     Place text
#     #                     )""")
#
#     def process_item(self, item, spider):
#         self.store_db(item)
#         return item
#
#     def store_db(self, item):
#         self.cursor.execute("""INSERT INTO tfrrs (AthleteName, Team, Location, EventDate, Event,
#         Performance, Place) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
#                             (
#                                 item.get('AthleteName'),
#                                 item.get('Team'),
#                                 item.get('Location'),
#                                 item.get('EventDate'),
#                                 item.get('Event'),
#                                 item.get('Performance'),
#                                 item.get('Place')
#                             ))
#         self.conn.commit()

class athletepipeline(object):

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
        self.cursor.execute("""DROP TABLE IF EXISTS athletes""")
        self.cursor.execute("""CREATE TABLE athletes (
                            season text
                            )""")

    def process_item(self, item, spider):
        self.store_db(athleteitem)
        return athleteitem

    def store_db(self, item):
        self.cursor.execute("""INSERT INTO athletes (season) VALUES (%s)""",
                            (
                                item.get('season')
                            ))
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
