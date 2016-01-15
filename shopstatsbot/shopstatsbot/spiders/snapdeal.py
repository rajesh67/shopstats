# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import json
from urlparse import urlparse,parse_qs
from .snapdeal_content_processor import SnapdealReviewContentProcessor
from scrapper.models import SnapdealReview

aff_id='4930'
aff_token='9731bfdba6f70d64b47a2abc7e69f7'
snapdeal_headers={'Snapdeal-Affiliate-Id':aff_id,'Snapdeal-Token-Id':aff_token,'Accept':'application/json'}
snapdeal_listings=['Cameras_Accessories','Mobiles_Tablets','Computers_Peripherals']

Mobiles_Tablets_Subcats=['Tablets','Mobile Phones']
Cameras_Accessories_Subcats=['Digital Cameras','DSLRs','Camcorders']
Computers_Peripherals_Subcats=['Monitors','Desktops','Laptops']

snapdeal_seed='snapdeal.{categoryId}.reviews.seeds.txt'


class SnapdealReviewSpider(CrawlSpider):
    name = "snapdeal_review_spider"
    allowed_domains = ["snapdeal.com"]
    start_urls = ['']

    rules=(
    	Rule(LinkExtractor(allow=('/product/(.*?)/(.*?)/reviews\?page=(?P<page_num>\d+)\&sortBy=(?P<sort_by>\w+)'),restrict_css=('div.reviewareain>a.btnload.LTgray','div.pagination>ul.LTblack>li>a.rippleGrey')),process_links='filter_links',callback='parse_reviews_pages',follow=True),
    )

    def __init__(self,categoryId,*args,**kwargs):
    	super(SnapdealReviewSpider,self).__init__(*args,**kwargs)
    	seeds=open(snapdeal_seed.format(categoryId=categoryId),'r')
    	start_urls=json.load(seeds)
    	seeds.close()
    	self.start_urls=start_urls
    	self.reviews_url=[]
    	self.first_pages_urls=start_urls[0]
    	self.content_processor=SnapdealReviewContentProcessor()

    def filter_links(self,links):
        for link in links:
            if link.url not in self.start_urls:
                self.reviews_url.append(link)
        return self.reviews_url

    def parse_reviews_pages(self, response):
    	print "** Reviews Pages **"
    	reviews=self.content_processor.process_response(response)
    	for review in reviews:
    		reviewId=review['reviewId']
    		snap_review,created=SnapdealReview.objects.get_or_create(reviewId=reviewId)
    		if created:
    			snap_review.reviewId=reviewId
    			snap_review.productId=review['productId']
    			snap_review.date=review['date']
    			snap_review.head=review['head']
    			snap_review.text=review['text']
    			snap_review.rating=int(review['rating'])
    			snap_review.certified=review['certified']
    			snap_review.username=review['user']
    			snap_review.save()
    		else:
    			print " Already Available Review "

    def parse_start_url(self,response):
    	print "++Start Url ++"
    	reviews=self.content_processor.process_response(response)
    	for review in reviews:
    		reviewId=review['reviewId']
    		snap_review,created=SnapdealReview.objects.get_or_create(reviewId=reviewId)
    		if created:
    			snap_review.reviewId=reviewId
    			snap_review.productId=review['productId']
    			snap_review.date=review['date']
    			snap_review.head=review['head']
    			snap_review.text=review['text']
    			snap_review.rating=int(review['rating'])
    			snap_review.certified=review['certified']
    			snap_review.username=review['user']
    			snap_review.save()
    		else:
    			print " Already Available Review "
    			
    def closed(self,reason):
    	print reason

class SnapdealSeedSpider(scrapy.Spider):
	name="snapdeal_seed_spider"
	allowed_domains=["snapdeal.com"]
	start_urls=["http://affiliate-feeds.snapdeal.com/feed/4930.json"]

	"""docstring for SnapdealSeedSpider"""
	def __init__(self, categoryId):
		super(SnapdealSeedSpider, self).__init__()
		self.categoryId=categoryId
		self.subcategories=[]
		self.reviews_urls=[]

	def parse(self,response):
		data=json.loads(response.body)
		listings=data['apiGroups']['Affiliate']['listingsAvailable']
		for key,listing in listings.iteritems():
			if key==self.categoryId:
				listing_url=listing['listingVersions']['v1']['get']
				request=scrapy.Request(url=listing_url,headers=snapdeal_headers,callback=self.parse_listing)
				yield request

	def parse_listing(self,response):
		data=json.loads(response.body)
		products=data['products']
		for product in products:
			subcat=product['subCategoryName']
			url=product['link'].split('?')[0]
			review_url=url+'/reviews?page=1&sortBy=RECENCY'
			if self.categoryId=='Mobiles_Tablets':
				if subcat in Mobiles_Tablets_Subcats:
					self.reviews_urls.append(review_url)
			elif self.categoryId=='Computers_Peripherals':
				if subcat in Computers_Peripherals_Subcats:
					self.reviews_urls.append(review_url)
			elif self.categoryId=='Cameras_Accessories':
				if subcat in Cameras_Accessories_Subcats:
					self.reviews_urls.append(review_url)
			else:
				pass
		if 'nextUrl' in data.keys():
			if data['nextUrl']:
				next_url=data['nextUrl']
				request=scrapy.Request(url=next_url,headers=snapdeal_headers,callback=self.parse_listing)
				yield request
			else:
				print products[products.__len__()-1]

	def closed(self,reason):
		print reason
		seeds=open(snapdeal_seed.format(categoryId=self.categoryId),'w')
		seeds.write(json.dumps(self.reviews_urls))
		seeds.close()