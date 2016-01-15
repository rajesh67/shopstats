

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
				


class SnapdealContentProcessor(object):

	"""docstring for SnapdealContentProcessor"""
	def __init__(self,):
		super(SnapdealContentProcessor, self).__init__()
		self.product=SnapdealProduct()

	def process_html_data(self):
		pass

class SnapdealReviewContentProcessor(object):
	"""docstring for SnapdealReviewContentProcessor"""
	def __init__(self):
		super(SnapdealReviewContentProcessor, self).__init__()

