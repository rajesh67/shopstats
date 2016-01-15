# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopstatsbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ReviewItem(scrapy.Item):
	reviewId=scrapy.Field()
	productId=scrapy.Field()
	reviewer=scrapy.Field()
	reviewer_url=scrapy.Field()
	certified=scrapy.Field()
	date=scrapy.Field()

	head=scrapy.Field()
	parmalink=scrapy.Field()
	review_text=scrapy.Field()
	rating=scrapy.Field()