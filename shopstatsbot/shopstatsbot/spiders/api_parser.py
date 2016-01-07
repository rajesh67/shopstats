import scrapy
import json
from os import listdir
from os.path import isfile,join
from datetime import datetime

from scrapy.spiders import CrawlSpider

FLIPKART_API_PRODUCT_FILE='products/flipkart/%s/%s'
FLIPKART_API_PRODUCT_PRICE_FILE='prices/snapdeal/%s/%s'

SNAPDEAL_API_PRODUCT_FILE='productsjson/snapdeal/%s/%s'
SNAPDEAL_API_PRODUCT_PRICE_FILE='prices/snapdeal/%s/%s'

PRICE_UPDATE_DATE_FORMAT='%A, %d. %B %Y %I:%M%p'


class FlipkartApiBot(CrawlSpider):
	name="FlipkartApiBot"
	allowed_domains=["flipkart.net"]

	start_urls=(
			'https://affiliate-api.flipkart.net/affiliate/api/rajeshmee.json',
		)
	"""docstring for FlipkartApiBot"""
	def __init__(self):
		super(FlipkartApiBot, self).__init__()
		self.aff_id='rajeshmee'
		self.aff_token='78fef03fe9d84c9eb6387b80ba4c98d2'
		self.api_json_url='https://affiliate-api.flipkart.net/affiliate/api/rajeshmee.json'

	def parse(self,response):
		json_data=json.loads(response.body)
		listings=json_data['apiGroups']['affiliate']['apiListings']
		data=json.loads(json.dumps(listings))
		for key,value in listings.iteritems():
			print "Proceesing Fetching Products for category **********%s********"%key
			category_url=value['availableVariants']['v0.1.0']['get']
			request=scrapy.Request(url=category_url,headers={'Fk-Affiliate-Id':self.aff_id,'Fk-Affiliate-Token':self.aff_token},callback=self.prase_categories)
			request.meta['categoryId']=key
			yield request

	def prase_categories(self,response):
		categoryId=response.meta['categoryId']
		parsed=json.loads(response.body)
		#now parse products from this url
		try:
			products=parsed['productInfoList']
			for product in products:
				self.save_poduct(product,categoryId)
			nextUrl=parsed['nextUrl']
			if nextUrl:
				request=scrapy.Request(url=nextUrl,headers={'Fk-Affiliate-Id':self.aff_id,'Fk-Affiliate-Token':self.aff_token},callback=self.prase_categories)
				request.meta['categoryId']=categoryId
				yield request
			else:
				print "Fetched all products for Category ****** %s *******"%categoryId
		except Exception, e:
			print "Somthing Went Wrong while fetching products"
			raise e

	def save_poduct(self,product,categoryId):
		productBaseInfo=product['productBaseInfo']
		productShippingBaseInfo=product['productShippingBaseInfo']
		offset=product=product['offset']

		productIdentifier=productBaseInfo['productIdentifier']
		productAttributes=productBaseInfo['productAttributes']

		shippingOptions=productShippingBaseInfo['shippingOptions']

		productId=productIdentifier['productId']
		categories=productIdentifier['categoryPaths']['categoryPath']

		productAttributes.update({'productId':productId,'categories':categories})

		product_file=FLIPKART_API_PRODUCT_FILE%(categoryId,productId)
		print product_file
		file_exists=isfile(product_file)
		if not file_exists:
			f=open(product_file,'w')
			f.write(json.dumps(productAttributes))
			f.close()




class SnapdealApiBot(CrawlSpider):
	name="SnapdealApiBot"
	allowed_domains=["snapdeal.com"]
	start_urls=(
		'http://affiliate-feeds.snapdeal.com/feed/4930.json',
	)

	"""docstring for SnapdealApiBot"""
	def __init__(self):
		super(SnapdealApiBot, self).__init__()
		self.aff_id='4930'
		self.aff_token='9731bfdba6f70d64b47a2abc7e69f7'
		self.special_category='World_Food_/_Indian_Food'

	def parse(self,response):
		json_data=json.loads(response.body)
		listings=json_data['apiGroups']['Affiliate']['listingsAvailable']
		for key,value in listings.iteritems():
			if key==self.special_category:
				categoryId='World_Food_Indian_Food'
				category_url=value['listingVersions']['v1']['get']
				request=scrapy.Request(url=category_url,headers={'Snapdeal-Affiliate-Id':self.aff_id,'Snapdeal-Token-Id':self.aff_token,'Accept':'application/json'},callback=self.parse_categories)
				request.meta['categoryId']=categoryId
				yield request
			else:
				categoryId=key
				category_url=value['listingVersions']['v1']['get']
				request=scrapy.Request(url=category_url,headers={'Snapdeal-Affiliate-Id':self.aff_id,'Snapdeal-Token-Id':self.aff_token,'Accept':'application/json'},callback=self.parse_categories)
				request.meta['categoryId']=categoryId
				yield request

	def parse_categories(self,response):
		categoryId=response.meta['categoryId']
		try:
			json_data=json.loads(response.body)
			products=json_data['products']
			for product in products:
				self.save_product(product,categoryId)
			nextUrl=json_data['nextUrl']
			if nextUrl:
				request=scrapy.Request(url=nextUrl,headers={'Snapdeal-Affiliate-Id':self.aff_id,'Snapdeal-Token-Id':self.aff_token,'Accept':'application/json'},callback=self.parse_categories)
				request.meta['categoryId']=categoryId
				yield request
			else:
				print "****************Fetched All Products for Category =%s********************"%categoryId

		except Exception, e:
			print "Something Went Wrong While Fetching catery %s"%categoryId
			raise e

	def save_product(self,product,categoryId):
		productId=product['id']

		product_file=SNAPDEAL_API_PRODUCT_FILE%(categoryId,productId)
		f=open(product_file,'w')
		out_data=json.dumps(product)
		f.write(out_data)
		f.close()
		print '{0}/{1}'.format(categoryId,productId)



class SnapdealSelectedApiBot(CrawlSpider):
	name="SnapdealSelectedApiBot"
	allowed_domains=["snapdeal.com"]
	start_urls=(
		'http://affiliate-feeds.snapdeal.com/feed/4930.json',
	)

	"""docstring for SnapdealSelectedApiBot"""
	def __init__(self,categoryId):
		super(SnapdealSelectedApiBot, self).__init__()
		self.categoryId=categoryId
		self.aff_id='4930'
		self.aff_token='9731bfdba6f70d64b47a2abc7e69f7'
		self.special_category='World_Food_/_Indian_Food'

	def parse(self,response):
		json_data=json.loads(response.body)
		listings=json_data['apiGroups']['Affiliate']['listingsAvailable']
		for key,value in listings.iteritems():
			if key==self.categoryId:
				category_url=value['listingVersions']['v1']['get']
				request=scrapy.Request(url=category_url,headers={'Snapdeal-Affiliate-Id':self.aff_id,'Snapdeal-Token-Id':self.aff_token,'Accept':'application/json'},callback=self.parse_categories)
				request.meta['categoryId']=self.categoryId
				yield request

	def parse_categories(self,response):
		categoryId=response.meta['categoryId']
		try:
			json_data=json.loads(response.body)
			products=json_data['products']
			for product in products:
				self.save_product_json(product,categoryId)
			nextUrl=json_data['nextUrl']
			if nextUrl:
				request=scrapy.Request(url=nextUrl,headers={'Snapdeal-Affiliate-Id':self.aff_id,'Snapdeal-Token-Id':self.aff_token,'Accept':'application/json'},callback=self.parse_categories)
				request.meta['categoryId']=categoryId
				yield request
			else:
				print "****************Fetched All Products for Category =%s********************"%categoryId

		except Exception, e:
			print "Something Went Wrong While Fetching catery %s"%categoryId
			raise e

	def save_product_json(self,product,categoryId):
		productId=product['id']
		mrp=product['mrp']
		price=product['offerPrice']
		if mrp and price:
			product_file=SNAPDEAL_API_PRODUCT_FILE%(categoryId,productId)
			file_exists=isfile(product_file)
			if not file_exists:
				f=open(price_file,'a')
				f.write(product)
				f.close()
			print product_file