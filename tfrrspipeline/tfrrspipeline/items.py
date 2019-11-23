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

class athletepipelineItem(scrapy.Item):
        season = scrapy.Field()
