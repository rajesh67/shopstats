# Create your views here.

import django
from django.http import HttpResponse,Http404
import os.path

from flipkart.models import FlipkartProduct
from django.core import serializers
import json

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.decorators.csrf import ensure_csrf_cookie

from .helpers import iterparse

#new supported api urls views
CATEGORIES_LIST=["mobiles","tablets","cameras","laptops","desktops"]
CATEGORIES_DICT={
	0:'all',
	1:'mobiles',
	2:'tablets',
	3:'cameras',
	4:'laptops',
	5:'desktops',
}

FLIPKART_PRODUCTS_JSON_FILE='products/flipkart/%s/%s'
FLIPKART_PRODUCTS_REVIEWS_JSON_FILE='reviews/flipkart/%s/%s'
FLIPKART_PRODUCTS_REVIEWS_BASE_DIR='reviews/flipkart/%s/'
FLIPKART_PRODUCTS_REVIEWS_ANALYZED_FILE='reviews/flipkart/%s/analyzed/%s'

FLIPKART_COMMON_CAMERAS_REVIEWS_FILE='cameras_reviews.json'
FLIPKART_COMMON_MOBILES_REVIEWS_FILE='mobiles_reviews.json'
FLIPKART_COMMON_TABLETS_REVIEWS_FILE=''
FLIPKART_COMMON_LAPTOPS_REVIEWS_FILE=''
FLIPKART_COMMON_DESKTOPS_REVIEWS_FILE=''


#returns all the products of a perticular category
@ensure_csrf_cookie
def category_list(request,categoryId):
	#list all the products for all categories
	products=FlipkartProduct.objects.all()
	if request.method=='GET':
		page=request.GET.get('page')
		filtered_products=[]
		if categoryId==CATEGORIES_LIST[0]:
			filtered_products=products.filter(categoryId=categoryId).order_by('-total_reviews').exclude(price__lte=10)
		elif categoryId==CATEGORIES_LIST[1]:
			filtered_products=products.filter(categoryId=categoryId).order_by('-total_reviews')
		elif categoryId==CATEGORIES_LIST[2]:
			filtered_products=products.filter(categoryId=categoryId).order_by('-total_reviews')
		elif categoryId==CATEGORIES_LIST[3]:
			filtered_products=products.filter(categoryId=categoryId).order_by('-total_reviews').exclude(price__lte=100)
		elif categoryId==CATEGORIES_LIST[4]:
			filtered_products=products.filter(categoryId=categoryId).order_by('-total_reviews').exclude(price__lte=100)
		else:
			return Http404
		paginator=Paginator(filtered_products,24)
		items=[]
		try:
			items=paginator.page(page)
		except PageNotAnInteger:
			items=paginator.page(1)
		except EmptyPage:
			items=paginator.page(paginator.num_pages)
		out_data=serializers.serialize('json',items)
		return HttpResponse(out_data,content_type="application/json")
	else:
		raise Http404

#returns product database data
@ensure_csrf_cookie
def product_database_data(request,categoryId,productId):
	if categoryId in CATEGORIES_LIST:
		#return product details from database
		try:
			product=FlipkartProduct.objects.get(product_id=productId)
			json_data=serializers.serialize('json',[product,])
			out_data=json.dumps(json_data)
			return HttpResponse(out_data,content_type="application/json")
		
		except FlipkartProduct.DoesNotExist:
			raise Http404
	else:
		raise Http404

#returns product json data 
@ensure_csrf_cookie
def product_json_data(request,categoryId,productId):
	product_file=FLIPKART_PRODUCTS_JSON_FILE%(categoryId,productId)
	try:
		pf=open(product_file,'r')
		json_data=json.load(pf)
		pf.close()
		out_data=json.dumps(json_data)
		return HttpResponse(out_data,content_type="application/json")
	except Exception, e:
		raise Http404

#returns product reviews json data
@ensure_csrf_cookie
def product_reviews(request,categoryId,productId):
	file_exists=os.path.isfile(os.path.join(FLIPKART_PRODUCTS_REVIEWS_BASE_DIR%categoryId,productId))
	if file_exists:
		#return reviews file data
		f=open(FLIPKART_PRODUCTS_REVIEWS_JSON_FILE%(categoryId,productId),'r')
		data=f.read()
		out_data=[]
		decoded_data=[d for d in iterparse(data)]
		for reviews in decoded_data:
			for review in reviews:
				review['review_text']=[text.strip() for text in review['review_text']]
				out_data.append(review)
		out_data=json.dumps(out_data)
		return HttpResponse(out_data,content_type="application/json")
	else:
		return Http404

@ensure_csrf_cookie
def product_reviews_analyzed(request,categoryId,productId):
	rev_file=FLIPKART_PRODUCTS_REVIEWS_ANALYZED_FILE%(categoryId,productId)
	file_exists=os.path.isfile(rev_file)
	if file_exists:
		f=open(rev_file,'r')
		json_data=json.load(f)
		f.close()
		out_data=json.dumps(json_data)
		return HttpResponse(out_data,content_type="application/json")
	else:
		return Http404















#old to not be supported views 
@ensure_csrf_cookie
def get_mobiles_list(request):
	if request.method=='GET':
		products=FlipkartProduct.objects.all()
		paginator=Paginator(products,24)
		page=request.GET.get('page')
		items=[]
		try:
			items=paginator.page(page)
		except PageNotAnInteger:
			items=paginator.page(1)
		except EmptyPage:
			items=paginator.page(paginator.num_pages)
		prod_list=serializers.serialize('json',items)
		return HttpResponse(prod_list,content_type="application/json")
	else:
		return HttpResponse("request method not valid")



@ensure_csrf_cookie
def get_product_url_by_id(request):
	if request.method=='GET':
		productId=request.GET.get('productId')
		product=FlipkartProduct.objects.get(product_id=productId)
		data=serializers.serialize('json',[product,])
		return HttpResponse(data,content_type="application/json")
	else:
		return HttpResponse("post request is not supported currently")

@ensure_csrf_cookie
def get_product(request,productId):
	if request.method=='GET':
		product=FlipkartProduct.objects.get(product_id=productId)
		data=serializers.serialize('json',[product,])
		return HttpResponse(data,content_type="application/json")
	else:
		return HttpResponse("post request is not supported currently")

@ensure_csrf_cookie
def get_json_file(request):
	if request.method=='GET':
		file_name=request.GET.get('file')
		file_name=file_name.strip()
		productId=request.GET.get('productId')

		rfile=open(file_name,'r')
		json_data=json.load(rfile)
		rfile.close()
		reviews=[]
		for review in json_data:
			if review['productId']==productId:
				text=review['review_text']
				stripped_text=[]
				for t in text:
					if t.strip():
						stripped_text.append(t.strip())
				review['review_text']=stripped_text
				reviews.append(review)

		data=json.dumps(reviews)
		return HttpResponse(data,content_type="application/json")
	else:
		return HttpResponse("post request not allowed")
