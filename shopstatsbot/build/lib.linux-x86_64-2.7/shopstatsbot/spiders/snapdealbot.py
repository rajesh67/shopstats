import scrapy
import csv

from .datamapper import SnapdealDataMapper

CAMERA_HTML_FILE='html/snapdeal/cameras/%s'
COMPUTER_PERIPHERALS_HTML_FILE='html/snapdeal/computer_peripherals/%s'
MOBILE_TABLETS_HTML_FILE='html/snapdeal/mobiles_tablets/%s'

class SnapdealCamerasBot(scrapy.Spider):
	name="SnapdealCamerasBot"
	allowed_domains=['snapdeal.com']
	
	"""docstring for SnapdealCamerasBot"""
	def __init__(self):
		super(SnapdealCamerasBot, self).__init__()
		datamapper=SnapdealDataMapper()
		cameras=datamapper.process_cameras_data()
		self.cameras=cameras

	def start_requests(self):
		for camera in self.cameras:
			try:
				request=scrapy.Request(camera['productUrl'],callback=self.parse)
				request.meta['productId']=camera['productId']
				yield request
			except Exception, e:
				print "Something Went Wrong Inside SnapdealCamerasBot start_requests() Function"

	def parse(self,response):
		productId=response.meta['productId']
		with open(CAMERA_HTML_FILE%productId,'wb') as hfile:
			hfile.write(response.body)
			hfile.close()


class SnapdealComputersBot(scrapy.Spider):
	name="SnapdealComputersBot"
	allowed_domains=['snapdeal.com']
	
	"""docstring for SnapdealComputersBot"""
	def __init__(self):
		super(SnapdealComputersBot, self).__init__()
		datamapper=SnapdealDataMapper()
		computers=datamapper.process_computer_peripherals_data()
		self.computers=computers[201:]

	def start_requests(self):
		for computer in self.computers:
			try:
				request=scrapy.Request(computer['productUrl'],callback=self.parse)
				request.meta['productId']=computer['productId']
				yield request
			except Exception, e:
				print "Something Went Wrong Inside SnapdealComputersBot start_requests() Function"

	def parse(self,response):
		productId=response.meta['productId']
		with open(COMPUTER_PERIPHERALS_HTML_FILE%productId,'wb') as hfile:
			hfile.write(response.body)
			hfile.close()


class SnapdealMobilesBot(scrapy.Spider):
	name="SnapdealMobilesBot"
	allowed_domains=['snapdeal.com']
	
	"""docstring for SnapdealMobilesBot"""
	def __init__(self):
		super(SnapdealMobilesBot, self).__init__()
		datamapper=SnapdealDataMapper()
		mobiles=datamapper.process_mobiles_tablets_data()
		self.mobiles=mobiles[201:100000]

	def start_requests(self):
		for mobile in self.mobiles:
			try:
				request=scrapy.Request(mobile['productUrl'],callback=self.parse)
				request.meta['productId']=mobile['productId']
				yield request
			except Exception, e:
				print "Something Went Wrong Inside SnapdealMobilesBot start_requests() Function"

	def parse(self,response):
		productId=response.meta['productId']
		with open(MOBILE_TABLETS_HTML_FILE%productId,'wb') as hfile:
			hfile.write(response.body)
			hfile.close()