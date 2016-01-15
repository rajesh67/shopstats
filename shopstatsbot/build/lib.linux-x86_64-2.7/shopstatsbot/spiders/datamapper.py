import csv
#from flipkart.models import FlipkartProduct
FlipkartProduct=''

SNAPDEAL_MOBILES_TABLETS_DATA_FILE='Data/Snapdeal/CSV/Mobiles_Tablets.csv'
SNAPDEAL_CAMERAS_ACCESSORIES_DATA_FILE='Data/Snapdeal/CSV/Cameras_Accessories.csv'
SNAPDEAL_COMPUTER_PERIPHERALS_DATA_FILE='Data/Snapdeal/CSV/Computers_Peripherals.csv'

FLIPKART_CAMERAS_DATA_FILE='Data/Flipkart/Cameras/jek-p31.csv'
FLIPKART_MOBILES_DATA_FILE='Data/Flipkart/Mobiles/tyy-4io.csv'
FLIPKART_TABLETS_DATA_FILE='Data/Flipkart/Tablets/tyy-hry.csv'
FLIPKART_LAPTOPS_DATA_FILE='Data/Flipkart/Laptops/6bo-b5g.csv'
FLIPKART_DESKTOPS_DATA_FILE='Data/Flipkart/Desktops/6bo-igk.csv'


class FlipkartDataMapper(object):
	
	"""docstring for FlipkartDataMapper"""
	def __init__(self):
		super(FlipkartDataMapper, self).__init__()
		self.cameras_data_file=FLIPKART_CAMERAS_DATA_FILE
		self.tablets_data_file=FLIPKART_TABLETS_DATA_FILE
		self.laptops_data_file=FLIPKART_LAPTOPS_DATA_FILE
		self.desktops_data_file=FLIPKART_DESKTOPS_DATA_FILE
		self.mobiles_data_file=FLIPKART_MOBILES_DATA_FILE

	def process_cameras_data(self):
		cameras=[]
		with open(self.cameras_data_file,'rb') as cfile:
			data=csv.reader(cfile,delimiter=',')
			for line in data:
				try:
					camera_data={'productId':'','productTitle':'','productUrl':''}
					camera_data['productId']=line[0]
					camera_data['productTitle']=line[1]
					camera_data['productUrl']=line[6]
					camera_data.update()
					cameras.append(camera_data)
				except Exception, e:
					print "Something Went Wrong"
			cfile.close()
		return cameras

	def process_tablets_data(self):
		tablets=[]
		with open(self.tablets_data_file,'rb') as tabfile:
			data=csv.reader(tabfile,delimiter=',')
			for line in data:
				try:
					tablet_data={'productId':'','productTitle':'','productUrl':''}
					tablet_data['productId']=line[0]
					tablet_data['productTitle']=line[1]
					tablet_data['productUrl']=line[6]
					tablet_data.update()
					tablets.append(tablet_data)
				except Exception, e:
					print "Something Went Wrong"
			tabfile.close()
		return tablets

	def process_mobiles_data(self):
		mobiles=[]
		with open(self.mobiles_data_file,'rb') as mfile:
			data=csv.reader(mfile,delimiter=',')
			for line in data:
				try:
					mobile_data={'productId':'','productTitle':'','productUrl':''}
					mobile_data['productId']=line[0]
					mobile_data['productTitle']=line[1]
					mobile_data['productUrl']=line[6]
					mobile_data.update()
					mobiles.append(mobile_data)
				except Exception, e:
					print "Something Went Wrong"
		mfile.close()
		return mobiles

	def process_desktops_data(self):
		desktops=[]
		with open(self.desktops_data_file,'rb') as dfile:
			data=csv.reader(dfile)
			for line in data:
				try:
					desktop_data={'productId':'','productTitle':'','productUrl':''}
					desktop_data['productId']=line[0]
					desktop_data['productTitle']=line[1]
					desktop_data['productUrl']=line[6]
					desktop_data.update()
					desktops.append(desktop_data)
				except Exception, e:
					raise e
			dfile.close()
		return desktops

	def process_laptops_data(self):
		laptops=[]
		with open(self.laptops_data_file,'rb') as lfile:
			data=csv.reader(lfile,delimiter=',')
			for line in data:
				try:
					laptop_data={'productId':'','productTitle':'','productUrl':''}
					laptop_data['productId']=line[0]
					laptop_data['productTitle']=line[1]
					laptop_data['productUrl']=line[6]
					laptop_data.update()
					laptops.append(laptop_data)
				except Exception, e:
					raise e
			lfile.close()
		return laptops

class SnapdealDataMapper(object):
	"""docstring for SnapdealDataMapper"""
	def __init__(self):
		super(SnapdealDataMapper, self).__init__()
		self.mobiles_tablets_data_file=SNAPDEAL_MOBILES_TABLETS_DATA_FILE
		self.cameras_data_file=SNAPDEAL_CAMERAS_ACCESSORIES_DATA_FILE
		self.computer_pheripherals_data_file=SNAPDEAL_COMPUTER_PERIPHERALS_DATA_FILE

	def process_computer_peripherals_data(self):
		computers=[]
		with open(self.computer_pheripherals_data_file,'rb') as compfile:
			data=csv.reader(compfile,delimiter='\t')
			for line in data:
				try:
					product_data={'productId':'','productTitle':'','productUrl':''}
					product_data['productId']=line[0]
					product_data['productTitle']=line[1]
					product_data['productUrl']=line[4]
					product_data.update()
					computers.append(product_data)
				except Exception, e:
					print "Error:While reading line in mobiles_tablets_snapdeal_file"
		compfile.close()
		return computers

	def process_mobiles_tablets_data(self):
		mobiles=[]
		with open(self.mobiles_tablets_data_file,'rb') as mtfile:
			data=csv.reader(mtfile,delimiter='\t')
			for line in data:
				try:
					product_data={'productId':'','productTitle':'','productUrl':''}
					product_data['productId']=line[0]
					product_data['productTitle']=line[1]
					product_data['productUrl']=line[4]
					product_data.update()
					mobiles.append(product_data)
				except Exception, e:
					print "Error:While reading line in mobiles_tablets_snapdeal_file"
			mtfile.close()
		return mobiles

	def process_cameras_data(self):
		cameras=[]
		with open(self.cameras_data_file,'rb') as csvfile:
			reader=csv.reader(csvfile,delimiter='\t')
			for line in reader:
				try:
					camera_data={'productId':'','productTitle':'','productUrl':''}
					camera_data['productId']=line[0]
					camera_data['productTitle']=line[1]
					camera_data['productUrl']=line[4]
					camera_data.update()
					cameras.append(camera_data)
				except Exception, e:
					print "Something Went Wrong"
			csvfile.close()
		return cameras



class FlipkartProductData(object):
	"""docstring for FlipkartProductData"""
	def __init__(self):
		super(FlipkartProductData, self).__init__()
		self.mobiles_data_file=FLIPKART_MOBILES_DATA_FILE
		self.cameras_data_file=FLIPKART_CAMERAS_DATA_FILE
		self.tablets_data_file=FLIPKART_TABLETS_DATA_FILE
		self.desktops_data_file=FLIPKART_DESKTOPS_DATA_FILE
		self.laptops_data_file=FLIPKART_LAPTOPS_DATA_FILE

	def process_mobiles_data(self):
		mobiles=[]
		with open(self.mobiles_data_file,'rb') as mfile:
			data=csv.reader(mfile,delimiter=',')
			for line in data:
				try:
					mobile_data={}
					mobile_data['productId']=line[0]
					mobile_data['productTitle']=line[1]
					mobile_data['description']=line[2]
					mobile_data['imageUrl']=line[3]
					mobile_data['mrp']=line[4]
					mobile_data['price']=line[5]
					mobile_data['productUrl']=line[6]
					mobile_data['categories']=line[7]
					mobile_data['brand']=line[8]
					mobile_data['deliverytime']=line[9]
					mobile_data['instock']=line[10]
					mobile_data['codAvailable']=line[11]
					mobile_data['emiAvailable']=line[12]
					mobile_data['offers']=line[13]
					mobile_data['discount']=line[14]
					mobile_data['cashBack']=line[15]
					mobile_data['size']=line[16]
					mobile_data['color']=line[17]
					mobile_data['sizeUnit']=line[18]
					mobile_data['sizeVarients']=line[19]
					mobile_data['colorvarients']=line[20]
					mobile_data['styleCode']=line[21]
					mobile_data.update()
					mobiles.append(mobile_data)
				except Exception, e:
					print "Something Went Wrong"
		mfile.close()
		return mobiles

	def process_tablets_data(self):
		mobiles=[]
		with open(self.tablets_data_file,'rb') as mfile:
			data=csv.reader(mfile,delimiter=',')
			for line in data:
				try:
					mobile_data={}
					mobile_data['productId']=line[0]
					mobile_data['productTitle']=line[1]
					mobile_data['description']=line[2]
					mobile_data['imageUrl']=line[3]
					mobile_data['mrp']=line[4]
					mobile_data['price']=line[5]
					mobile_data['productUrl']=line[6]
					mobile_data['categories']=line[7]
					mobile_data['brand']=line[8]
					mobile_data['deliverytime']=line[9]
					mobile_data['instock']=line[10]
					mobile_data['codAvailable']=line[11]
					mobile_data['emiAvailable']=line[12]
					mobile_data['offers']=line[13]
					mobile_data['discount']=line[14]
					mobile_data['cashBack']=line[15]
					mobile_data['size']=line[16]
					mobile_data['color']=line[17]
					mobile_data['sizeUnit']=line[18]
					mobile_data['sizeVarients']=line[19]
					mobile_data['colorvarients']=line[20]
					mobile_data['styleCode']=line[21]
					mobile_data.update()
					mobiles.append(mobile_data)
				except Exception, e:
					print "Something Went Wrong"
		mfile.close()
		return mobiles

	def process_cameras_data(self):
		cameras=[]
		with open(self.cameras_data_file,'rb') as mfile:
			data=csv.reader(mfile,delimiter=',')
			for line in data:
				try:
					mobile_data={}
					mobile_data['productId']=line[0]
					mobile_data['productTitle']=line[1]
					mobile_data['description']=line[2]
					mobile_data['imageUrl']=line[3]
					mobile_data['mrp']=line[4]
					mobile_data['price']=line[5]
					mobile_data['productUrl']=line[6]
					mobile_data['categories']=line[7]
					mobile_data['brand']=line[8]
					mobile_data['deliverytime']=line[9]
					mobile_data['instock']=line[10]
					mobile_data['codAvailable']=line[11]
					mobile_data['emiAvailable']=line[12]
					mobile_data['offers']=line[13]
					mobile_data['discount']=line[14]
					mobile_data['cashBack']=line[15]
					mobile_data['size']=line[16]
					mobile_data['color']=line[17]
					mobile_data['sizeUnit']=line[18]
					mobile_data['sizeVarients']=line[19]
					mobile_data['colorvarients']=line[20]
					mobile_data['styleCode']=line[21]
					mobile_data.update()
					cameras.append(mobile_data)
				except Exception, e:
					print "Something Went Wrong"
		mfile.close()
		return cameras

	def process_laptops_data(self):
		laptops=[]
		with open(self.laptops_data_file,'rb') as mfile:
			data=csv.reader(mfile,delimiter=',')
			for line in data:
				try:
					mobile_data={}
					mobile_data['productId']=line[0]
					mobile_data['productTitle']=line[1]
					mobile_data['description']=line[2]
					mobile_data['imageUrl']=line[3]
					mobile_data['mrp']=line[4]
					mobile_data['price']=line[5]
					mobile_data['productUrl']=line[6]
					mobile_data['categories']=line[7]
					mobile_data['brand']=line[8]
					mobile_data['deliverytime']=line[9]
					mobile_data['instock']=line[10]
					mobile_data['codAvailable']=line[11]
					mobile_data['emiAvailable']=line[12]
					mobile_data['offers']=line[13]
					mobile_data['discount']=line[14]
					mobile_data['cashBack']=line[15]
					mobile_data['size']=line[16]
					mobile_data['color']=line[17]
					mobile_data['sizeUnit']=line[18]
					mobile_data['sizeVarients']=line[19]
					mobile_data['colorvarients']=line[20]
					mobile_data['styleCode']=line[21]
					mobile_data.update()
					laptops.append(mobile_data)
				except Exception, e:
					print "Something Went Wrong"
		mfile.close()
		return laptops

	def process_desktops_data(self):
		desktops=[]
		with open(self.desktops_data_file,'rb') as mfile:
			data=csv.reader(mfile,delimiter=',')
			for line in data:
				try:
					mobile_data={}
					mobile_data['productId']=line[0]
					mobile_data['productTitle']=line[1]
					mobile_data['description']=line[2]
					mobile_data['imageUrl']=line[3]
					mobile_data['mrp']=line[4]
					mobile_data['price']=line[5]
					mobile_data['productUrl']=line[6]
					mobile_data['categories']=line[7]
					mobile_data['brand']=line[8]
					mobile_data['deliverytime']=line[9]
					mobile_data['instock']=line[10]
					mobile_data['codAvailable']=line[11]
					mobile_data['emiAvailable']=line[12]
					mobile_data['offers']=line[13]
					mobile_data['discount']=line[14]
					mobile_data['cashBack']=line[15]
					mobile_data['size']=line[16]
					mobile_data['color']=line[17]
					mobile_data['sizeUnit']=line[18]
					mobile_data['sizeVarients']=line[19]
					mobile_data['colorvarients']=line[20]
					mobile_data['styleCode']=line[21]
					mobile_data.update()
					desktops.append(mobile_data)
				except Exception, e:
					print "Something Went Wrong"
		mfile.close()
		return desktops

class FlipkartDatabaseMapper(object):
	"""docstring for FlipkartDatabaseMapper"""
	def __init__(self):
		super(FlipkartDatabaseMapper, self).__init__()
		productData=FlipkartProductData()
		self.mobiles=productData.process_mobiles_data()
		self.cameras=productData.process_cameras_data()
		self.tablets=productData.process_tablets_data()
		self.desktops=productData.process_desktops_data()
		self.laptops=productData.process_laptops_data()

	def process_mobiles_data_into_database(self):
		for mobile in self.mobiles[1:]:
			product,created=FlipkartProduct.objects.get_or_create(product_id=mobile['productId'])
			if created:
				product.categoryId="mobiles"
				product.product_id=mobile['productId']
				product.product_url=mobile['productUrl']
				product.product_title=mobile['productTitle']
				product.description=mobile['description']
				product.images=mobile['imageUrl'].split(';')
				mrp=mobile['mrp']
				price=mobile['price']
				discount=mobile['discount']
				if mrp:
					print 'mrp=%s'%mrp
					product.mrp=float(mrp)
				if price:
					product.price=float(price)
				if discount:
					product.discount=float(discount)
				product.categories=mobile['categories']
				product.brand=mobile['brand']
				product.delivery_time=mobile['deliverytime']
				product.instock=bool(mobile['instock'])
				emiAvailable=mobile['emiAvailable']
				codAvailable=mobile['codAvailable']
				product.emi_available=bool(emiAvailable)
				product.cod_available=bool(codAvailable)

				product.offers=mobile['offers']
				cashback=mobile['cashBack']
				if cashback:
					product.cashback=float(cashback)
				size=mobile['size']
				if size:
					product.size=size
				product.sizeunit=mobile['sizeUnit']

				colors=mobile['colorvarients']
				colors=colors.replace('[','')
				colors=colors.replace(']','')
				colors=colors.split(',')
				product.color_varients=colors				
				sizes=mobile['sizeVarients']
				sizes=sizes.replace('[','')
				sizes=sizes.replace(']','')
				sizes=sizes.split(',')
				product.size_varients=sizes
				product.color=mobile['color']
				product.stylecode=mobile['styleCode']
				product.save()
			else:
				product.categoryId="mobiles"
				product.save()

	def process_cameras_data_into_database(self):
		for camera in self.cameras[1:]:
			product,created=FlipkartProduct.objects.get_or_create(product_id=camera['productId'])
			if created:
				product.categoryId="cameras"
				product.product_id=camera['productId']
				product.product_url=camera['productUrl']
				product.product_title=camera['productTitle']
				product.description=camera['description']
				product.images=camera['imageUrl'].split(';')
				mrp=camera['mrp']
				price=camera['price']
				discount=camera['discount']
				if mrp:
					print 'mrp=%s'%mrp
					product.mrp=float(mrp)
				if price:
					product.price=float(price)
				if discount:
					product.discount=float(discount)
				product.categories=camera['categories']
				product.brand=camera['brand']
				product.delivery_time=camera['deliverytime']
				product.instock=bool(camera['instock'])
				emiAvailable=camera['emiAvailable']
				codAvailable=camera['codAvailable']
				product.emi_available=bool(emiAvailable)
				product.cod_available=bool(codAvailable)

				product.offers=camera['offers']
				cashback=camera['cashBack']
				if cashback:
					product.cashback=float(cashback)
				size=camera['size']
				if size:
					product.size=size
				product.sizeunit=camera['sizeUnit']

				colors=camera['colorvarients']
				colors=colors.replace('[','')
				colors=colors.replace(']','')
				colors=colors.split(',')
				product.color_varients=colors

				sizes=camera['sizeVarients']
				sizes=sizes.replace('[','')
				sizes=sizes.replace(']','')
				sizes=sizes.split(',')
				product.size_varients=sizes

				product.color=camera['color']
				product.stylecode=camera['styleCode']
				product.save()
			else:
				product.categoryId="cameras"
				product.save()

	def process_tablets_data_into_database(self):
		for mobile in self.tablets[1:]:
			product,created=FlipkartProduct.objects.get_or_create(product_id=mobile['productId'])
			if created:
				product.categoryId="tablets"
				product.product_id=mobile['productId']
				product.product_url=mobile['productUrl']
				product.product_title=mobile['productTitle']
				product.description=mobile['description']
				product.images=mobile['imageUrl'].split(';')
				mrp=mobile['mrp']
				price=mobile['price']
				discount=mobile['discount']
				if mrp:
					print 'mrp=%s'%mrp
					product.mrp=float(mrp)
				if price:
					product.price=float(price)
				if discount:
					product.discount=float(discount)
				product.categories=mobile['categories']
				product.brand=mobile['brand']
				product.delivery_time=mobile['deliverytime']
				product.instock=bool(mobile['instock'])
				emiAvailable=mobile['emiAvailable']
				codAvailable=mobile['codAvailable']
				product.emi_available=bool(emiAvailable)
				product.cod_available=bool(codAvailable)

				product.offers=mobile['offers']
				cashback=mobile['cashBack']
				if cashback:
					product.cashback=float(cashback)
				size=mobile['size']
				if size:
					product.size=size
				product.sizeunit=mobile['sizeUnit']

				colors=mobile['colorvarients']
				colors=colors.replace('[','')
				colors=colors.replace(']','')
				colors=colors.split(',')
				product.color_varients=colors				
				sizes=mobile['sizeVarients']
				sizes=sizes.replace('[','')
				sizes=sizes.replace(']','')
				sizes=sizes.split(',')
				product.size_varients=sizes
				product.color=mobile['color']
				product.stylecode=mobile['styleCode']
				product.save()
			else:
				product.categoryId="tablets"
				product.save()

	def process_laptops_data_into_database(self):
		for mobile in self.laptops[1:]:
			product,created=FlipkartProduct.objects.get_or_create(product_id=mobile['productId'])
			if created:
				product.categoryId="laptops"
				product.product_id=mobile['productId']
				product.product_url=mobile['productUrl']
				product.product_title=mobile['productTitle']
				product.description=mobile['description']
				product.images=mobile['imageUrl'].split(';')
				mrp=mobile['mrp']
				price=mobile['price']
				discount=mobile['discount']
				if mrp:
					print 'mrp=%s'%mrp
					product.mrp=float(mrp)
				if price:
					product.price=float(price)
				if discount:
					product.discount=float(discount)
				product.categories=mobile['categories']
				product.brand=mobile['brand']
				product.delivery_time=mobile['deliverytime']
				product.instock=bool(mobile['instock'])
				emiAvailable=mobile['emiAvailable']
				codAvailable=mobile['codAvailable']
				product.emi_available=bool(emiAvailable)
				product.cod_available=bool(codAvailable)

				product.offers=mobile['offers']
				cashback=mobile['cashBack']
				if cashback:
					product.cashback=float(cashback)
				size=mobile['size']
				if size:
					product.size=size
				product.sizeunit=mobile['sizeUnit']

				colors=mobile['colorvarients']
				colors=colors.replace('[','')
				colors=colors.replace(']','')
				colors=colors.split(',')
				product.color_varients=colors				
				sizes=mobile['sizeVarients']
				sizes=sizes.replace('[','')
				sizes=sizes.replace(']','')
				sizes=sizes.split(',')
				product.size_varients=sizes
				product.color=mobile['color']
				product.stylecode=mobile['styleCode']
				product.save()
			else:
				product.categoryId="laptops"
				product.save()

	def process_desktops_data_into_database(self):
		for mobile in self.desktops[1:]:
			product,created=FlipkartProduct.objects.get_or_create(product_id=mobile['productId'])
			if created:
				product.categoryId="desktops"
				product.product_id=mobile['productId']
				product.product_url=mobile['productUrl']
				product.product_title=mobile['productTitle']
				product.description=mobile['description']
				product.images=mobile['imageUrl'].split(';')
				mrp=mobile['mrp']
				price=mobile['price']
				discount=mobile['discount']
				if mrp:
					print 'mrp=%s'%mrp
					product.mrp=float(mrp)
				if price:
					product.price=float(price)
				if discount:
					product.discount=float(discount)
				product.categories=mobile['categories']
				product.brand=mobile['brand']
				product.delivery_time=mobile['deliverytime']
				product.instock=bool(mobile['instock'])
				emiAvailable=mobile['emiAvailable']
				codAvailable=mobile['codAvailable']
				product.emi_available=bool(emiAvailable)
				product.cod_available=bool(codAvailable)

				product.offers=mobile['offers']
				cashback=mobile['cashBack']
				if cashback:
					product.cashback=float(cashback)
				size=mobile['size']
				if size:
					product.size=size
				product.sizeunit=mobile['sizeUnit']

				colors=mobile['colorvarients']
				colors=colors.replace('[','')
				colors=colors.replace(']','')
				colors=colors.split(',')
				product.color_varients=colors				
				sizes=mobile['sizeVarients']
				sizes=sizes.replace('[','')
				sizes=sizes.replace(']','')
				sizes=sizes.split(',')
				product.size_varients=sizes
				product.color=mobile['color']
				product.stylecode=mobile['styleCode']
				product.save()
			else:
				product.categoryId="desktops"
				product.save()