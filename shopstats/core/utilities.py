from os import listdir
from os.path import join,isfile
from urlparse import urljoin

FLIPKART_BASE_URL='http://www.flipkart.com'

FLIPKART_CERTIFIED_BUYER_IMAGE_URL='http://img6a.flixcart.com/www/prod/images/certified_buyer-e6c64f39.png'
FLIPKART_ADVANTAGE_IMAGE_URL='http://img5a.flixcart.com/www/prod/images/fbf-logo-new-1b256010.png'
FLIPKART_FIRST_TO_REVIEW_IMAGE_URL='http://img6a.flixcart.com/www/prod/images/first_to_review-0567206d.png'


FLIPLART_MOBILES_HTML_FILES='html/flipkart/mobiles/%s'
FLIPLART_CAMERAS_HTML_FILES='html/flipkart/cameras/%s'
FLIPLART_DESKTOPS_HTML_FILES='html/flipkart/desktops/%s'
FLIPLART_LAPTOPS_HTML_FILES='html/flipkart/laptops/%s'
FLIPLART_TABLETS_HTML_FILES='html/flipkart/tablets/%s'

FLIPLART_MOBILES_HTML_FILES_DIR='html/flipkart/mobiles/'
FLIPLART_CAMERAS_HTML_FILES_DIR='html/flipkart/cameras/'
FLIPLART_DESKTOPS_HTML_FILES_DIR='html/flipkart/desktops/'
FLIPLART_LAPTOPS_HTML_FILES_DIR='html/flipkart/laptops/'
FLIPLART_TABLETS_HTML_FILES_DIR='html/flipkart/tablets/'

import re
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

class FlipkartHtmlLocater(object):

	"""docstring for FlipkartHtmlLocater"""
	def __init__(self):
		super(FlipkartHtmlLocater, self).__init__()
		self.mobiles_html_files=FLIPLART_MOBILES_HTML_FILES_DIR
		self.cameras_html_files=FLIPLART_CAMERAS_HTML_FILES_DIR
		self.laptops_html_files=FLIPLART_LAPTOPS_HTML_FILES_DIR
		self.desktops_html_files=FLIPLART_DESKTOPS_HTML_FILES_DIR
		self.tablets_html_files=FLIPLART_TABLETS_HTML_FILES_DIR

	def find_mobiles_html_file(self):
		onlyfiles=[]
		onlyfiles=[f for f in listdir(self.mobiles_html_files) if isfile(join(self.mobiles_html_files,f))]
		return onlyfiles
	
	def find_cameras_html_file(self):
		onlyfiles=[]
		onlyfiles=[f for f in listdir(self.cameras_html_files) if isfile(join(self.cameras_html_files,f))]
		return onlyfiles

	def find_tablets_html_files(self):
		onlyfiles=[]
		onlyfiles=[f for f in listdir(self.tablets_html_files) if isfile(join(self.tablets_html_files,f))]
		return onlyfiles

	def find_desktops_html_files(self):
		onlyfiles=[]
		onlyfiles=[f for f in listdir(self.desktops_html_files) if isfile(join(self.desktops_html_files,f))]
		onlyfiles

	def find_laptops_html_files(self):
		onlyfiles=[]
		onlyfiles=[f for f in listdir(self.laptops_html_files) if isfile(join(self.laptops_html_files,f))]
		return onlyfiles


class FlipkartElelectronicsContentProcessor(object):

	"""docstring for FlipkartElelectronicsContentProcessor"""
	def __init__(self):
		super(FlipkartElelectronicsContentProcessor, self).__init__()
		self.productId=''
		self.productTitle=''
		self.productUrl=''

		self.seller={'name':'','url':'','total_ratings':0,'ratings':0,'badge':''}
		self.specifications={
			'GENERAL FEATURES':[],
			'Camera':[],
			'Multimedia':[],
			'Internet & Connectivity':[],
			'Other Features':[],
			'Warranty':[],
			'Display':[],
			'Dimensions':[],
			'Battery':[],
			'Memory and Storage':[],
			'Platform':[],
			'Important Note':''
		}
		self.numofReviews=0
		self.reviews_url=''

		self.sellers_url=''

	def __dict__(self):
		return {
			'id':self.productId,
			'title':self.productTitle,
			'url':self.prodcutUrl,
			'seller':self.seller,
			'reviews_url':self.reviews_url,
			'sellers_url':self.sellers_url,
			'specs':self.specifications,
		}

	def process_response(self,response):
		
		def _normalize_url(url):
			return urljoin(FLIPKART_BASE_URL,url)

		def _get_title(self):
			try:
				title=response.css('h1.title::text').extract()[0].strip()
				self.productTitle=title
				return True
			except Exception, e:
				print "Title Does Not Exist for this product"
				return False

		def _get_specifications(self):
			#functions used within this scope

			def _spec_key(x,specs):
				try:
					self.specifications[x]=specs
				except KeyError:
					print "Specification Head not Defined Plese add this to known heads"

			for table in response.css('div.productSpecs').css('table.specTable'):
				head=table.css('th.groupHead::text').extract()[0].strip()
				specs=[]
				for row in table.css('tr')[1:]:
					try:
						key=row.css('td.specsKey::text').extract()[0].strip()
						value=row.css('td.specsValue::text').extract()[0].strip()
						specs.append({'key':key,'value':value})
					except Exception,e:
						#not working correctly
						value1=row.css('td.specsValue>ul.valueList>li::text').extract()
						_spec_key(head,value1)
				#now set this in specifications
				_spec_key(head,specs)

		def _get_reviews_url(self):
			text=''
			try:
				text=response.css('div.askReview>a::text').extract()[0].strip()
			except Exception, e:
				print "AskReviews div not found"

			if text=='Be the first to write a Review':
				self.reviews_url=''
				self.numofReviews=0
				try:
					url=response.css('div.subLine>p.subText>a::attr(href)').extract()[0]
					self.reviewer_url=_normalize_url(url)
				except Exception, e:
					print "product url doesn't exist"

			elif text=='Write a Review':
				url=response.css('div.subLine>p.subText>a::attr(href)').extract()[0]
				self.reviews_url=_normalize_url(url)
			else:
				print "this product doesn't have askReview div productId=%s"%response.meta['productId']

		def _get_seller(self):
			
			#function within this local scope
			def _seller_key(x,value):
				try:
					self.seller[x]=value
				except KeyError:
					print "Key Error in seller extract"

			#try to get the profile_url and reviewer name
			try:
				url=response.css('a.seller-name::attr(href)').extract()[0]
				name=response.css('a.seller-name::text').extract()[0].strip()
				_seller_key('name',name)
				_seller_key('url',_normalize_url(url))
			except Exception, e:
				print "couldn't Get seller information"

			#get seller ratings of of five
			try:
				ratings=response.css('span.rating-out-of-five::text').extract()[0]
				if ratings=='New Seller!':
					print "New Seller"
				elif ratings:
					scores=[f.strip() for f in ratings.strip().split('/')]
					_seller_key('ratings',scores[0])
				else:
					print "print Something Went Wrong while fetching seller ratings"
			except Exception,e:
				print "Couldn't find seller rating"
			
			#get seller badge
			try:
				badge=response.css('span.fk-advantage')
				if badge:
					_seller_key('badge','fk-advantage')
			except Exception, e:
				print "Couldn't get seller badge"
			
			#get sellers total ratings
			try:
				total_ratings=response.css('div.sellerRatingCount>span>span.fk-text-right::text').extract()
				if total_ratings:
					s=total_ratings[0]
					s=s.replace('(','')
					s=s.replace(')','')
					s=s.replace('ratings','')
					_seller_key('total_ratings',locale.atoi(s))
			except Exception,e:
				print "Couldn't get total_ratings of seller"

		def _get_prices(self):
			pass

		self.prodcutUrl=response.url
		self.productId=response.meta['productId']
		if _get_title(self):
			_get_specifications(self)
			_get_reviews_url(self)
			_get_seller(self)

class FlipkartProductReview(object):
	
	"""docstring for FlipkartProductReview"""
	def __init__(self):
		super(FlipkartProductReview, self).__init__()
		self.productId=''
		self.reviewer=''
		self.reviewer_url=''
		self.review_text=''
		self.rating=0
		self.parmalink=''
		self.certified_buyer=False
		self.first_review=False
		self.head=''
		self.date=''

	def __dict__(self):
		return {
			'productId':self.productId,
			'reviewer':self.reviewer,
			'reviewer_url':self.reviewer_url,
			'rating':self.rating,
			'parmalink':self.parmalink,
			'head':self.head,
			'review_text':self.review_text,
			'certified':self.certified_buyer,
			'first_review':self.first_review,
			'date':self.date,
		}

class FlipkartReviewsProcessor(object):
	"""docstring for FlipkartReviewsProcessor"""
	def __init__(self):
		super(FlipkartReviewsProcessor, self).__init__()

	def process_response(self,response):
		
		def _normalize_url(url):
			return urljoin(FLIPKART_BASE_URL,url)

		def _get_review_detail(review_box,review):
			#local functions within this scope
			def _product_reviewer():
				try:
					name=review_box.css('a.load-user-widget::text').extract()
					url=review_box.css('a.load-user-widget::attr(href)').extract()
					review.reviewer_url=url
					review.reviewer=name
				except Exception, e:
					name=review_box.css('span.review-userName::text').extract()
					url=review_box.css('a.load-user-widget::attr(href)').extract()
					review.reviewer_url=url
					review.reviewer=name
				else:
					pass
				finally:
					date_div1=review_box.css('p.review-date::text')
					date_div2=review_box.css('div.date::text')
					if date_div1:
						review.date=date_div1.extract()[0]
					else:
						review.date=date_div2.extract()[0]
			def _certified_reviewer():
				try:
					certified=review_box.css('img.img::attr(alt)').extract()[0]
					first_review=review_box.css('img.firstReviewerBadge::attr(alt)').extract()[0]
					if certified=='certified buyer':
						review.certified_buyer=True
					elif first_review=='First to review':
						review.first_review=True
					else:
						pass
						
				except Exception, e:
					print "Couldn't get certificate of reviewer"

			def _review_rating():
				try:
					rating=review_box.css('div.fk-stars::attr(title)').extract()[0]
					rating=re.search('\d+',rating).group()
					review.rating=locale.atoi(rating)
				except Exception, e:
					print "Couldn't get rating for this reviewer %s"%review.reviewer
			
			def _review_parmalink():
				try:
					url=review_box.css('div.unitExt>a::attr(href)').extract()[0]
					review.parmalink=_normalize_url(url)
				except Exception, e:
					print "couldn't find permalink for this review"
			def _review_text():
				try:
					text=review_box.css('span.review-text::text').extract()
					review.review_text=text
				except Exception, e:
					print "Could not find review text"
			
			def _review_head():
				try:
					head=review_box.css('div.bmargin5>strong::text').extract()[0].strip()
					review.head=head
				except Exception, e:
					print "could not found head for review url=%s"%review.parmalink

			#now apply all the above functions
			review.productId=response.meta['productId']
			_product_reviewer()
			_certified_reviewer()
			_review_rating()
			_review_parmalink()
			_review_text()
			_review_head()
			#successfully applied all the function on review

		def _numOf_total_reviews(self):
			try:
				n=response.css('div.review-section-info>h3>span::text').extract()[0]
				n=n.replace('(','')
				n=n.replace(')','')
				n=locale.atoi(n)
				print "Total Number of Reviews=%s"%n
			except Exception, e:
				print "reviews_count not found"

		reviews=[]
		r_list=response.css('div.fk-review')
		for review_box in r_list:
			review=FlipkartProductReview()
			_get_review_detail(review_box,review)
			reviews.append(review.__dict__())
		return reviews