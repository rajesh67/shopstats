# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor


flipkart_affid='rajeshmee'
flipkart_token='78fef03fe9d84c9eb6387b80ba4c98d2'
flipkart_headers={'Fk-Affiliate-Id':flipkart_affid,'Fk-Affiliate-Token':flipkart_token}
flipkart_categories=["tablets","mobiles","laptops","cameras","desktops","laptops"]


class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["flipkart.net"]
    start_urls = (
    	'https://affiliate-api.flipkart.net/affiliate/api/rajeshmee.json',
    )
    def __init__(self):
    	super(FlipkartSpider,self).__init__()

    def parse(self, response):
    	json_data=json.loads(response.body)
    	listings=json_data['apiGroups']['affiliate']['apiListings']
    	for categoryId in flipkart_categories:
    		print "Currently Getting category={category}".format(category=categoryId)
    		listing_url=listings[categoryId]['availableVariants']['v0.1.0']['get']
    		request=scrapy.Request(url=listing_url,headers=flipkart_headers,callback=self.parse_category)
    		request.meta['categoryId']=categoryId
    		yield request

    def parse_category(self,response):
    	categoryId=response.meta['categoryId']
    	products_data=json.loads(response.body)
    	product_list=products_data['productInfoList']
    	for product in product_list:
    		identifiers=product['productBaseInfo']['productIdentifier']
    		attributes=product['productBaseInfo']['productAttributes']
    		print attributes.keys()
    		productId=identifiers['productId']
    		categoryPaths=identifiers['categoryPaths']
    		title=attributes['title']
    		print " product title ======%s=========== and productId=*******%s******"%(title,productId)

    	if 'nextUrl' in products_data.keys():
    		nextUrl=products_data['nextUrl']
    		if nextUrl:
    			request=scrapy.Request(url=nextUrl,headers=flipkart_headers,callback=self.parse_category)
    			request.meta['categoryId']=categoryId
    			yield request


class FlipkartReviewsSpider(CrawlSpider):
	name="flipkartreviewsspider"
	allowed_domains=["flipkart.com"]
	start_urls=[
		'http://www.flipkart.com/samsung-galaxy-j7/product-reviews/ITMEAFBFJHSYDBPW?pid=MOBE93GWSMGZHFSK&type=all',
	]
	rules=(
		Rule(LinkExtractor(allow=('/(.*?)/product-reviews/(.*?)',),restrict_css=('div.fk-navigation>a',),), callback='parse_next_page_reviews',process_links='filter_links',follow=True),
	)

	def __init__(self,*args,**kwargs):
		super(FlipkartReviewsSpider,self).__init__(*args,**kwargs)
		self.reviews_url=[]

	def parse_next_page_reviews(self,response):
		print response.url

	def filter_links(self,links):
		for link in links:
			if link not in self.reviews_url:
				self.reviews_url.append(link)
		return self.reviews_url

class FlipkartPriceSpider(scrapy.Spider):
	name="flipkartpricespider"
	allowed_domains=["flipkart.com"]
	start_urls=(
		'https://affiliate-api.flipkart.net/affiliate/api/rajeshmee.json',
	)

	"""docstring for FlipkartPriceSpider"""
	def __init__(self):
		super(FlipkartPriceSpider, self).__init__()

	def parse(self,response):
		json_data=json.loads(response.body)
		listings=json_data['apiGroups']['affiliate']['apiListings']
		for listing in listings:
			print listing