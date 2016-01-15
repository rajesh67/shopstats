

SNAPDEAL_MOBILES_TABLETS_DATA_FILE='Data/Snapdeal/CSV/Mobiles_Tablets.csv'
SNAPDEAL_CAMERAS_ACCESSORIES_DATA_FILE='Data/Snapdeal/CSV/Cameras_Accessories.csv'
SNAPDEAL_COMPUTER_PERIPHERALS_DATA_FILE='Data/Snapdeal/CSV/Computers_Peripherals.csv'

CAMERA_HTML_FILE='html/snapdeal/cameras/%s'
COMPUTER_PERIPHERALS_HTML_FILE='html/snapdeal/computer_peripherals/%s'
MOBILE_TABLETS_HTML_FILE='html/snapdeal/mobiles_tablets/%s'


class SnapdealProduct(object):
	"""docstring for SnapdealProduct"""
	def __init__(self):
		super(SnapdealProduct, self).__init__()

		self.productId=''
		self.productTitle=''
		self.productUrl=''
		self.mrp=0
		self.discount=0
		self.price=0

		self.offer=''
		self.specifications=[]
		self.reviews=[]

		self.seller=[]
		self.varients=[]

class SnapdealReview(object):
	"""docstring for SnapdealReview"""
	def __init__(self):
		super(SnapdealReview, self).__init__()
		self.productId=''
		self.reviewId=''
		self.date=''
		self.rating=''
		self.head=''
		self.text=''
		self.user=''
		self.certified=''
	def __dict__(self):
		return {
			'productId':self.productId,
			'reviewId':self.reviewId,
			'date':self.date,
			'rating':self.rating,
			'head':self.head,
			'text':self.text,
			'user':self.user,
			'certified':self.certified
		}
class SnapdealReviewContentProcessor(object):
	"""docstring for SnapdealReviewContentProcessor"""
	def __init__(self):
		super(SnapdealReviewContentProcessor, self).__init__()

	def process_response(self,response):
		productId=response.url.split('/')[-2]
		comments=response.css('div.commentreview').css('div.commentlist')
		reviews=[]
		for comment in comments:
			review=SnapdealReview()
			comment_id=comment.css('::attr(id)').extract()[0].split('_')[0]
			review.productId=productId
			review.reviewId=comment_id
			reviewer=comment.css('span._reviewUserName::attr(title)').extract()
			if reviewer:
				review.user=reviewer[0]
			verification=comment.css('.sd-icon-security-checked-filled-2')
			if verification:
				review.certified=True
			else:
				review.certified=False
			div=comment.css('.user-review')

			date=div.css('.date::text').extract()
			if date:
				review.date=date[0]
			review.rating=div.css('.rating').css('.sd-icon').__len__()
			head=div.css('.head::text').extract()
			if head:
				review.head=head[0]

			text=div.css('p::text').extract()
			if text:
				sentence=text[0].replace('\n',' ')
				review.text=sentence
			reviews.append(review.__dict__())
		return reviews