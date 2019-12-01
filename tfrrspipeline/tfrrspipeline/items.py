# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ImagesPipelineItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()

class rosterpipelineItem(scrapy.Item):
    gender = scrapy.Field()
    season = scrapy.Field()
    rosterteam = scrapy.Field()
    rosterurl = scrapy.Field()
    rostername = scrapy.Field()
    grade = scrapy.Field()
    seasonorder = scrapy.Field()

class resultspipelineItem(scrapy.Item):
    resultname = scrapy.Field()
    resulturl = scrapy.Field()
    team = scrapy.Field()
    location = scrapy.Field()
    eventdate = scrapy.Field()
    event = scrapy.Field()
    performance = scrapy.Field()
    place = scrapy.Field()
