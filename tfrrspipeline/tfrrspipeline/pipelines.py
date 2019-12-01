# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html and
# https://www.youtube.com/watch?v=6VFMGthBD58

# See more info here: http://scrapingauthority.com/scrapy-database-pipeline/
import scrapy
import mysql.connector
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import NotConfigured
from tfrrspipeline.items import rosterpipelineItem
from tfrrspipeline.items import ImagesPipelineItem
from tfrrspipeline.items import resultspipelineItem

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
        self.cursor.execute("""DROP TABLE IF EXISTS rosters""")
        self.cursor.execute("""CREATE TABLE rosters (
                            gender text,
                            season text,
                            rosterteam text,
                            rosterurl text,
                            rostername text,
                            grade text,
                            seasonorder text
                            )""")
        self.cursor.execute("""DROP TABLE IF EXISTS athleteresults""")
        self.cursor.execute("""CREATE TABLE athleteresults (
                            resultname text,
                            resulturl text,
                            team text,
                            location text,
                            eventdate text,
                            event text,
                            performance text,
                            place text
                            )""")

    def process_item(self, item, spider):
        if isinstance(item, rosterpipelineItem):
            self.store_db_roster(item)
            return item
        elif isinstance(item, resultspipelineItem):
            self.store_db_results(item)
            return item
        else:
            return item

    def store_db_results(self, item):
        self.cursor.execute("""INSERT INTO athleteresults (resultname, resulturl, team, location, eventdate, event, performance, place)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                            (
                                item.get('resultname'),
                                item.get('resulturl'),
                                item.get('team'),
                                item.get('location'),
                                item.get('eventdate'),
                                item.get('event'),
                                item.get('performance'),
                                item.get('place')
                            ))
        self.conn.commit()

    def store_db_roster(self, item):
        self.cursor.execute("""INSERT INTO rosters (gender, season, rosterteam, rosterurl, rostername, grade, seasonorder)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (
                                item.get('gender'),
                                item.get('season'),
                                item.get('rosterteam'),
                                item.get('rosterurl'),
                                item.get('rostername'),
                                item.get('grade'),
                                item.get('seasonorder')
                            ))
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
