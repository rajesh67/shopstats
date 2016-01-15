import scrapy
from scrapy.spiders import CrawlSpider

FlipkartHtmlLocater=''
FlipkartProduct=''

from .datamapper import FlipkartDataMapper

CAMERA_HTML_FILE='html/flipkart/cameras/%s'
MOBILES_HTML_FILE='html/flipkart/mobiles/%s'
DESKTOPS_HTML_FIEL='html/flipkart/desktops/%s'
LAPTOPS_HTML_FILE='html/flipkart/laptops/%s'
TABLETS_HTML_FILE='html/flipkart/tablets/%s'

FILE_URL_PATH='file:///home/raju/Downloads/December2015/shopstats/%s'

class FlipkartCamerasBot(scrapy.Spider):
	name="FlipkartCamerasBot"
	allowed_domains=["flipkart.com"]
	
	"""docstring for FlipkartCamerasBot"""
	def __init__(self):
		super(FlipkartCamerasBot, self).__init__()
		datamapper=FlipkartDataMapper()
		cameras=datamapper.process_cameras_data()
		self.cameras=cameras
		
	def start_requests(self):
		for camera in self.cameras:
			try:
				url=camera['productUrl']
				request=self.make_requests_from_url(url)
				request.meta['productId']=camera['productId']
				yield request
			except Exception, e:
				print "Some Error Occured"

	def parse(self,response):
		productId=response.meta['productId']
		try:
			with open(CAMERA_HTML_FILE%productId,'w+x') as hfile:
				hfile.write(response.body)
				hfile.close()
		except Exception, e:
			print "File Already Exists"
		yield

class FlipkartMobilesBot(scrapy.Spider):
	name="FlipkartMobilesBot"
	allowed_domains=["flipkart.com"]
	
	"""docstring for FlipkartMobilesBot"""
	def __init__(self):
		super(FlipkartMobilesBot, self).__init__()
		datamapper=FlipkartDataMapper()
		mobiles=datamapper.process_mobiles_data()
		self.mobiles=mobiles[320:]

	def start_requests(self):
		for mobile in self.mobiles:
			try:
				url=mobile['productUrl']
				request=self.make_requests_from_url(url)
				request.meta['productId']=mobile['productId']
				yield request
			except Exception, e:
				print "Some Error Occured"

	def parse(self,response):
		productId=response.meta['productId']
		try:
			with open(MOBILES_HTML_FILE%productId,'w+x') as hfile:
				hfile.write(response.body)
				hfile.close()
		except Exception, e:
			print "File Already Exists"


class FlipkartTabletsBot(scrapy.Spider):
	name="FlipkartTabletsBot"
	allowed_domains=["flipkart.com"]
	
	"""docstring for FlipkartTabletsBot"""
	def __init__(self):
		super(FlipkartTabletsBot, self).__init__()
		datamapper=FlipkartDataMapper()
		tablets=datamapper.process_tablets_data()
		self.tablets=tablets

	def start_requests(self):
		for tablet in self.tablets:
			try:
				url=tablet['productUrl']
				request=self.make_requests_from_url(url)
				request.meta['productId']=tablet['productId']
				yield request
			except Exception, e:
				print "Some Error Occured"

	def parse(self,response):
		productId=response.meta['productId']
		try:
			with open(TABLETS_HTML_FILE%productId,'w+x') as hfile:
				hfile.write(response.body)
				hfile.close()
		except Exception, e:
			print "File Already Exists"


class FlipkartDesktopsBot(scrapy.Spider):
	name="FlipkartDesktopsBot"
	allowed_domains=["flipkart.com"]
	
	"""docstring for FlipkartDesktopsBot"""
	def __init__(self):
		super(FlipkartDesktopsBot, self).__init__()
		datamapper=FlipkartDataMapper()
		desktops=datamapper.process_desktops_data()
		self.desktops=desktops
		
	def start_requests(self):
		for desktop in self.desktops:
			try:
				url=desktop['productUrl']
				request=self.make_requests_from_url(url)
				request.meta['productId']=desktop['productId']
				yield request
			except Exception, e:
				print "Some Error Occured"

	def parse(self,response):
		productId=response.meta['productId']
		try:
			with open(DESKTOPS_HTML_FIEL%productId,'w+x') as hfile:
				hfile.write(response.body)
				hfile.close()
		except Exception, e:
			print "File Already Exists"


class FlipkartLaptopsBot(scrapy.Spider):
	name="FlipkartLaptopsBot"
	allowed_domains=["flipkart.com"]
	
	"""docstring for FlipkartLaptopsBot"""
	def __init__(self):
		super(FlipkartLaptopsBot, self).__init__()
		datamapper=FlipkartDataMapper()
		laptops=datamapper.process_laptops_data()
		self.laptops=laptops[201:]
		
	def start_requests(self):
		for laptop in self.laptops:
			try:
				url=laptop['productUrl']
				request=self.make_requests_from_url(url)
				request.meta['productId']=laptop['productId']
				yield request
			except Exception, e:
				print "Some Error Occured"

	def parse(self,response):
		productId=response.meta['productId']
		try:
			with open(LAPTOPS_HTML_FILE%productId,'w+x') as hfile:
				hfile.write(response.body)
				hfile.close()
		except Exception, e:
			print "File Already Exists"


class FlipkartFileScrapper(scrapy.Spider):
	name="FlipkartFileScrapper"
	allowed_domains=['']


	"""docstring for FlipkartFileScrapper"""
	def __init__(self):
		super(FlipkartFileScrapper, self).__init__()
		self.locator=FlipkartHtmlLocater()

	def start_requests(self):
		files=self.locator.find_mobiles_html_file()
		for i in files:
			mobile_file=MOBILES_HTML_FILE%i
			url=FILE_URL_PATH%mobile_file
			request=scrapy.Request(url=url,callback=self.parse)
			request.meta['productId']=i
			yield request

	def parse(self,response):
		title=response.css('h1.title::text')
		try:
			print title.extract()[0]
		except Exception, e:
			print "Title Does not exist"