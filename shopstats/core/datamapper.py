DATA_DIR='apiProducts/%s/%s/' #store,#category
DATA_FILE='apiProducts/%s/%s/%s' #store,#category,#filename

from os import listdir
import json


class SnapdealSavedDataMapper(object):
	
	"""docstring for SnapdealSavedDataMapper"""
	def __init__(self):
		super(SnapdealSavedDataMapper, self).__init__()
		self.store='snapdeal'

	def list_category_files(self,categoryId):
		self.categoryId=categoryId
		self.data_dir=DATA_DIR%(self.store,categoryId)
		self.files=listdir(self.data_dir)
		self.total_products=self.files.__len__()
		print "Found total {0} products".format(self.total_products)

	def process_data(self):
		cat_file=open(self.categoryId,'a')
		for key,productId in enumerate(self.files):
			print "Processing {0}/{1} file".format(key,self.total_products)
			product_file=DATA_FILE%(self.store,self.categoryId,productId)
			f=open(product_file,'r')
			json_data=json.loads(f.read())
			f.close()
			print "============== product %s =============="%productId
			category=json_data['categoryName']
			subcategory=json_data['subCategoryName']
			cat_file.write(json.dumps({'categoryName':category,'subCategoryName':subcategory}))
		cat_file.close()

	def store_in_db(self):
		pass