import scrapy
#from flipkart.models import FlipkartProduct
FlipkartProduct=''
import os.path

FlipkartHtmlLocater=''
FlipkartElelectronicsContentProcessor=''
FlipkartReviewsProcessor=''

import json
from urlparse import urlparse,parse_qs,urlunparse,urljoin
from urllib import urlencode

from shopstatsbot.items import ReviewItem
from scrapy.spiders import CrawlSpider

HTML_FILES_BASE_URL='file:///home/raju/Downloads/December2015/shopstats/%s'

FLIPLART_PRODUCT_HTML_FILE='html/flipkart/%s/%s'
FLIPLART_PRODUCT_JSON_FILE='products/flipkart/%s/%s'
FLIPLART_PRODUCT_REVIEWS_FILE='reviews/flipkart/%s/%s'


FLIPLART_MOBILES_HTML_FILES='html/flipkart/mobiles/%s'
FLIPLART_CAMERAS_HTML_FILES='html/flipkart/cameras/%s'
FLIPLART_DESKTOPS_HTML_FILES='html/flipkart/desktops/%s'
FLIPLART_LAPTOPS_HTML_FILES='html/flipkart/laptops/%s'
FLIPLART_TABLETS_HTML_FILES='html/flipkart/tablets/%s'

FLIPLART_MOBILES_REVIEWS_FILES='reviews/flipkart/mobiles/%s'
FLIPLART_CAMERAS_REVIEWS_FILES='reviews/flipkart/cameras/%s'
FLIPLART_DESKTOPS_REVIEWS_FILES='reviews/flipkart/desktops/%s'
FLIPLART_LAPTOPS_REVIEWS_FILES='reviews/flipkart/laptops/%s'
FLIPLART_TABLETS_REVIEWS_FILES='reviews/flipkart/tablets/%s'

FLIPLART_MOBILES_HTML_FILES='html/flipkart/mobiles/%s'
FLIPLART_CAMERAS_HTML_FILES='html/flipkart/cameras/%s'
FLIPLART_DESKTOPS_HTML_FILES='html/flipkart/desktops/%s'
FLIPLART_LAPTOPS_HTML_FILES='html/flipkart/laptops/%s'
FLIPLART_TABLETS_HTML_FILES='html/flipkart/tablets/%s'

FLIPLART_MOBILES_PRODUCT_FILES='products/flipkart/mobiles/%s'
FLIPLART_CAMERAS_PRODUCT_FILES='products/flipkart/cameras/%s'
FLIPLART_DESKTOPS_PRODUCT_FILES='products/flipkart/desktops/%s'
FLIPLART_LAPTOPS_PRODUCT_FILES='products/flipkart/laptops/%s'
FLIPLART_TABLETS_PRODUCT_FILES='products/flipkart/tablets/%s'

class FlipkartHtmlBot(CrawlSpider):
	name="FlipkartHtmlProductBot"
	allowed_domains=['flipkart.com']

	"""docstring for FlipkartHtmlBot"""
	def __init__(self,):
		super(FlipkartHtmlBot, self).__init__()
		self.locator=FlipkartHtmlLocater()

	def start_requests(self):
		files=self.locator.find_cameras_html_file()
		for f in files:
			bfile=FLIPLART_CAMERAS_HTML_FILES%f
			request=scrapy.Request(url=HTML_FILES_BASE_URL%bfile,callback=self.parse)
			request.meta['productId']=f
			yield request

	def parse(self,response):
		productId=response.meta['productId']
		ecp=FlipkartElelectronicsContentProcessor()
		ecp.process_response(response)
		product=ecp.__dict__()
		
		print "--------%s------"%product['title']
		try:
			with open(FLIPLART_CAMERAS_PRODUCT_FILES%product['id'],'w+b') as pfile:
				pfile.write(json.dumps(product))
			pfile.close()
		
		except Exception, e:
			print "Product json could not be written"

		if product['reviews_url']:
			request=scrapy.Request(url=product['reviews_url'],callback=self.parse_first_page_reviews)
			request.meta['productId']=productId
			request.meta['reviews_url']=product['reviews_url']
			yield request

	def parse_first_page_reviews(self,response):

		#functions within this scope
		def _numOf_total_reviews():
			try:
				n=response.css('div.review-section-info>h3>span::text').extract()[0]
				n=n.replace('(','')
				n=n.replace(')','')
				print "Total Number of Reviews=%s"%n
				return int(n.strip())
			except Exception, e:
				print "reviews_count not be found"
				return 0

		productId=response.meta['productId']
		numOfReviews=_numOf_total_reviews()
		
		BASE_URL=response.meta['reviews_url']+'&rating=1,2,3,4,5&reviewers=all&sort=most_helpful&start=%d'

		if numOfReviews>10:
			product=FlipkartProduct.objects.get(product_id=productId)
			product.total_reviews=numOfReviews
			product.save()
			for i in xrange(10,numOfReviews,10):
				next_review_url=BASE_URL%i
				request=scrapy.Request(url=next_review_url,callback=self.next_pages_reviews)
				request.meta['productId']=productId
				yield request
		else:
			product=FlipkartProduct.objects.get(product_id=productId)
			product.total_reviews=numOfReviews
			product.save()

			#else extract reviews if they are on the first page
			frp=FlipkartReviewsProcessor()
			reviews=frp.process_response(response)
			for review in reviews:
				item=ReviewItem()
				item['date']=review['date']
				item['productId']=productId
				item['reviewer']=review['reviewer']
				item['reviewer_url']=review['reviewer_url']
				item['head']=review['head']
				item['certified']=review['certified']
				item['rating']=review['rating']
				item['parmalink']=review['parmalink']
				item['review_text']=review['review_text']
				yield item

	def next_pages_reviews(self,response):
		productId=response.meta['productId']
		frp=FlipkartReviewsProcessor()
		reviews=frp.process_response(response)
		for review in reviews:
			item=ReviewItem()
			item['date']=review['date']
			item['productId']=productId
			item['reviewer']=review['reviewer']
			item['reviewer_url']=review['reviewer_url']
			item['head']=review['head']
			item['certified']=review['certified']
			item['rating']=review['rating']
			item['parmalink']=review['parmalink']
			item['review_text']=review['review_text']
			yield item


class FlipkartOnlineReviewsBot(CrawlSpider):
	name="FlipkartOnlineReviewsBot"
	allowed_domains=['flipkart.com']

	"""docstring for FlipkartOnlineReviewsBot"""
	def __init__(self,categoryId=''):
		super(FlipkartOnlineReviewsBot, self).__init__()
		self.locator=FlipkartHtmlLocater()
		self.products=FlipkartProduct.objects.filter(categoryId=categoryId)
		self.categoryId=categoryId

	def start_requests(self):
		for product in self.products:
			request=scrapy.Request(url=product.product_url,callback=self.parse)
			request.meta['productId']=product.product_id
			yield request
	
	def parse(self,response):
		productId=response.meta['productId']
		
		product=self.products.get(product_id=productId)
		if product.product_url!=response.url:
			product.product_url=response.url
			product.save()

		#save html
		htmlfile=open(FLIPLART_PRODUCT_HTML_FILE%(self.categoryId,productId),'w+b')
		htmlfile.write(response.body)
		htmlfile.close()

		#extract product from the response
		fecp=FlipkartElelectronicsContentProcessor()
		fecp.process_response(response)
		json_product=fecp.__dict__()

		#write json data of the product
		data_file=FLIPLART_PRODUCT_JSON_FILE%(self.categoryId,productId)
		dfile=open(data_file,'w+b')
		dfile.write(json.dumps(json_product))
		dfile.close()

		#overhead of one crwal for every product
		#now extract reviews depends only if product have more than 10 reviews
		if json_product['reviews_url']:
			request=scrapy.Request(url=json_product['reviews_url'],callback=self.parse_first_page_reviews)
			request.meta['productId']=productId
			request.meta['reviews_url']=json_product['reviews_url']
			yield request
		else:
			#extract this page reviews
			print "Reviews URL does not exist for productId=%s"%productId

	def parse_first_page_reviews(self,response):
		productId=response.meta['productId']
		def _numOf_total_reviews():
			try:
				n=response.css('div.review-section-info>h3>span::text').extract()[0]
				n=n.replace('(','')
				n=n.replace(')','')
				print "Total Number of Reviews=%s"%n
				return int(n.strip())
			except Exception, e:
				print "reviews_count not be found"
				return 0
		#fix this function 
		def _next_page_base_reviews_url(reviewer_url,start):
			from urlparse import urlparse,parse_qs,urlunparse,urljoin
			from urllib import urlencode
			url_data=urlparse(reviewer_url)
			qs_data=parse_qs(url_data.query)
			if not 'start' in qs_data:
				qs_data['start']=[start]
			else:
				qs_data['start']=['start']

			url_data=url_data._replace(query=urlencode(qs_data,True))
			url=urlunparse(url_data)
			return url

		numOfReviews=_numOf_total_reviews()
		base_url=response.meta['reviews_url'].split('&')[0]

		next_url='%s&sort=most_helpful&start=%d&reviewers=all&type=all&rating=1,2,3,4,5'

		product=self.products.get(product_id=productId)
		if numOfReviews and product.total_reviews!=numOfReviews:
			product.total_reviews=numOfReviews
			product.save()

		reviews=[]		
		if numOfReviews>10:
			frp=FlipkartReviewsProcessor()
			reviews=frp.process_response(response)
			for review in reviews:
				item=ReviewItem()
				item['date']=review['date']
				item['productId']=productId
				item['reviewer']=review['reviewer']
				item['reviewer_url']=review['reviewer_url']
				item['head']=review['head']
				item['certified']=review['certified']
				item['rating']=review['rating']
				item['parmalink']=review['parmalink']
				item['review_text']=review['review_text']
				yield item

			for i in xrange(0,numOfReviews,10):
				request=scrapy.Request(url=next_url%(base_url,i),callback=self.parse_next_page_reviews)
				request.meta['productId']=productId
				yield request
		else:
			
			#now extract all the reviews on this page
			frp=FlipkartReviewsProcessor()
			reviews=frp.process_response(response)
			for review in reviews:
				item=ReviewItem()
				item['date']=review['date']
				item['productId']=productId
				item['reviewer']=review['reviewer']
				item['reviewer_url']=review['reviewer_url']
				item['head']=review['head']
				item['certified']=review['certified']
				item['rating']=review['rating']
				item['parmalink']=review['parmalink']
				item['review_text']=review['review_text']
				yield item
			#now save the reviews in review file
			rfile=open(FLIPLART_PRODUCT_REVIEWS_FILE%(self.categoryId,productId),'w+b')
			rfile.write(json.dumps(reviews))
			rfile.close()

	def parse_next_page_reviews(self,response):
		productId=response.meta['productId']
		
		frp=FlipkartReviewsProcessor()
		reviews=frp.process_response(response)
		for review in reviews:
			item=ReviewItem()
			item['date']=review['date']
			item['productId']=productId
			item['reviewer']=review['reviewer']
			item['reviewer_url']=review['reviewer_url']
			item['head']=review['head']
			item['certified']=review['certified']
			item['rating']=review['rating']
			item['parmalink']=review['parmalink']
			item['review_text']=review['review_text']
			yield item
		#now store in json file
		file_name=FLIPLART_PRODUCT_REVIEWS_FILE%(self.categoryId,productId)
		write_file=open(file_name,'a')
		write_file.write(json.dumps(reviews))
		write_file.close()