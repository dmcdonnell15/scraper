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

# PIPELINE 2: Team rosters
class rosterpipeline(object):

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

    def process_item(self, rosteritem, spider):
        if isinstance(rosteritem, rosterpipelineItem):
            self.store_db_roster(rosteritem)
            return rosteritem

    def store_db_roster(self, rosteritem):
        self.cursor.execute("""INSERT INTO rosters (gender, season, rosterteam, rosterurl, rostername, grade, seasonorder)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (
                                rosteritem.get('gender'),
                                rosteritem.get('season'),
                                rosteritem.get('rosterteam'),
                                rosteritem.get('rosterurl'),
                                rosteritem.get('rostername'),
                                rosteritem.get('grade'),
                                rosteritem.get('seasonorder')
                            ))
        self.conn.commit()

# PIPELINE 3: Athlete results
class resultspipeline(object):

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

    def process_item(self, resultsitem, spider):
        if isinstance(resultsitem, resultspipelineItem):
            self.store_db_results(resultsitem)
            return resultsitem

    def store_db_results(self, resultsitem):
        self.cursor.execute("""INSERT INTO athleteresults (resultname, resulturl, team, location, eventdate, event, performance, place)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                            (
                                resultsitem.get('resultname'),
                                resultsitem.get('resulturl'),
                                resultsitem.get('team'),
                                resultsitem.get('location'),
                                resultsitem.get('eventdate'),
                                resultsitem.get('event'),
                                resultsitem.get('performance'),
                                resultsitem.get('place')
                            ))
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
