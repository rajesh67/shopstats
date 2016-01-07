from django.conf.urls import patterns,include,url

urlpatterns=patterns('api.views',
	url(r'^products/$','get_mobiles_list',name="product-list"),
	url(r'^product/(?P<productId>[0-9a-zA-Z]+)/$','get_product',name="product-url"),
	url(r'^product/$','get_product_url_by_id',name="product-detail"),
	url(r'^json/files/$','get_json_file',name="json-file"),

	#supported api urls
	url(r'^(?P<categoryId>[0-9a-zA-Z]+)/products/$','category_list',name='category-list'),
	url(r'^(?P<categoryId>[0-9a-zA-Z]+)/product/(?P<productId>[0-9a-zA-Z]+)/db/$','product_database_data',name='product-database-data'),
	url(r'^(?P<categoryId>[0-9a-zA-Z]+)/product/(?P<productId>[0-9a-zA-Z]+)/json/$','product_json_data',name='product-json-data'),
	url(r'^(?P<categoryId>[0-9a-zA-Z]+)/product/(?P<productId>[0-9a-zA-Z]+)/reviews/$','product_reviews',name='product-reviews'),
	url(r'^(?P<categoryId>[0-9a-zA-Z]+)/product/(?P<productId>[0-9a-zA-Z]+)/reviews/analyzed/$','product_reviews_analyzed',name='product-analyzed-reviews'),
)	