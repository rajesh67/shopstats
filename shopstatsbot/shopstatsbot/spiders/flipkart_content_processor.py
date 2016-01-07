
FLIPKART_CAMERAS_DATA_FILE='Data/Flipkart/Cameras/jek-p31.csv'
FLIPKART_MOBILES_DATA_FILE='Data/Flipkart/Mobiles/tyy-4io.csv'
FLIPKART_TABLETS_DATA_FILE='Data/Flipkart/Tablets/tyy-hry.csv'
FLIPKART_LAPTOPS_DATA_FILE='Data/Flipkart/Laptops/6bo-b5g.csv'
FLIPKART_DESKTOPS_DATA_FILE='Data/Flipkart/Desktops/6bo-igk.csv'


class FlipkartProduct(object):
	"""docstring for FlipkartProduct"""
	def __init__(self):
		super(FlipkartProduct, self).__init__()
		self.productId=''
		self.productTitle=''
		self.productUrl=''

		self.mrp=0
		self.discount=0
		self.price=0

		self.reviews=[]
		self.specifications=[]
		self.seller=[]



class FlipkartContentProcessor(object):
	"""docstring for FlipkartContentProcessor"""
	def __init__(self):
		super(FlipkartContentProcessor, self).__init__()

	def process_html_data(self):
		pass