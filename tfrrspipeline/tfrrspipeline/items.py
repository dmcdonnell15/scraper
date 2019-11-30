# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# class TFRRSpipelineItem(scrapy.Item):
#         AthleteName = scrapy.Field()
#         Grade = scrapy.Field()
#         Team = scrapy.Field()
#         Location = scrapy.Field()
#         EventDate = scrapy.Field()
#         Event = scrapy.Field()
#         Performance = scrapy.Field()
#         Place = scrapy.Field()

class rosterpipelineItem(scrapy.Item):
        gender = scrapy.Field()
        season = scrapy.Field()
        teamname = scrapy.Field()
        athleteurl = scrapy.Field()
        athletename = scrapy.Field()
        grade = scrapy.Field()
        seasonorder = scrapy.Field()

class ImagesPipelineItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
