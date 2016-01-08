# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
#from flipkart.models import FlipkartBaseProduct

flipkart_affid='rajeshmee'
flipkart_token='78fef03fe9d84c9eb6387b80ba4c98d2'
flipkart_headers={'Fk-Affiliate-Id':flipkart_affid,'Fk-Affiliate-Token':flipkart_token}
flipkart_categories=["tablets","mobiles","laptops","cameras","desktops","laptops"]
reviews_seed_file='flipkart.{categoryId}.reviews.seeds.txt'

class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["flipkart.net"]
    start_urls = (
    	'https://affiliate-api.flipkart.net/affiliate/api/rajeshmee.json',
    )
    def __init__(self):
    	super(FlipkartSpider,self).__init__()

    def parse(self, response):
    	json_data=json.loads(response.body)
    	listings=json_data['apiGroups']['affiliate']['apiListings']
    	for categoryId in flipkart_categories:
    		print "Currently Getting category={category}".format(category=categoryId)
    		listing_url=listings[categoryId]['availableVariants']['v0.1.0']['get']
    		request=scrapy.Request(url=listing_url,headers=flipkart_headers,callback=self.parse_category)
    		request.meta['categoryId']=categoryId
    		yield request

    def parse_category(self,response):
    	categoryId=response.meta['categoryId']
    	products_data=json.loads(response.body)
    	product_list=products_data['productInfoList']
    	for product in product_list:
    		identifiers=product['productBaseInfo']['productIdentifier']
    		attributes=product['productBaseInfo']['productAttributes']
    		print attributes.keys()
    		productId=identifiers['productId']
    		categoryPaths=identifiers['categoryPaths']
    		title=attributes['title']
    		print " product title ======%s=========== and productId=*******%s******"%(title,productId)

    	if 'nextUrl' in products_data.keys():
    		nextUrl=products_data['nextUrl']
    		if nextUrl:
    			request=scrapy.Request(url=nextUrl,headers=flipkart_headers,callback=self.parse_category)
    			request.meta['categoryId']=categoryId
    			yield request

class FlipkartPriceSpider(scrapy.Spider):
	name="flipkartpricespider"
	allowed_domains=["flipkart.com"]
	start_urls=(
		'https://affiliate-api.flipkart.net/affiliate/api/rajeshmee.json',
	)

	"""docstring for FlipkartPriceSpider"""
	def __init__(self):
		super(FlipkartPriceSpider, self).__init__()

	def parse(self,response):
		json_data=json.loads(response.body)
		listings=json_data['apiGroups']['affiliate']['apiListings']
		for listing in listings:
			print listing

class FlipkartReviewsSpider(CrawlSpider):
    name="flipkartreviewsspider"
    allowed_domains=["flipkart.net","flipkart.com"]
    start_urls=[]
    rules=(Rule(LinkExtractor(allow=('/(.*?)/product-reviews/(.*?)',),restrict_css=('div.fk-navigation>a',),), callback='parse_next_page_reviews',process_links='filter_links',follow=True),)

    def __init__(self,categoryId,*args,**kwargs):
        super(FlipkartReviewsSpider,self).__init__(*args,**kwargs)
        self.reviews_url=[]
        self.categoryId=categoryId
        s_file=open(reviews_seed_file.format(categoryId=categoryId),'r')
        urls=json.load(s_file)
        s_file.close()
        self.start_urls=urls

    def parse_next_page_reviews(self,response):
        print response.url

    def filter_links(self,links):
        for link in links:
            if link not in self.reviews_url:
                self.reviews_url.append(link)
        return self.reviews_url

class FlipkartSeedSpider(scrapy.Spider):
    name="flipkartseedspider"
    allowed_domains=["flipkart.net"]
    start_urls=(
        'https://affiliate-api.flipkart.net/affiliate/api/rajeshmee.json',
    )

    """docstring for FlipkartSeedSpider"""
    def __init__(self,categoryId,*args,**kwargs):
        super(FlipkartSeedSpider, self).__init__(*args,**kwargs)
        self.categoryId=categoryId
        self.product_urls=[]

    def parse(self,response):
        category_listings=json.loads(response.body)
        categories=category_listings['apiGroups']['affiliate']['apiListings']
        listing_url=categories[self.categoryId]['availableVariants']['v0.1.0']['get']
        request=scrapy.Request(url=listing_url,headers=flipkart_headers,callback=self.parse_products_url)
        yield request

    def parse_products_url(self,response):
        products_data=json.loads(response.body)
        products=products_data['productInfoList']
        for product in products:
            productId=product['productBaseInfo']['productIdentifier']['productId']
            productUrl=product['productBaseInfo']['productAttributes']['productUrl']
            parts=productUrl.split('/p/')
            cap_letters=parts[-1].split('?')
            url='http://www.flipkart.com/'+parts[0].split('/dl/')[-1]+'/product-reviews/'+cap_letters[0].upper()+'?'+cap_letters[-1]+'&type=all'
            if url not in self.product_urls:
                self.product_urls.append(url)
        if 'nextUrl' in products_data.keys():
            yield scrapy.Request(url=products_data['nextUrl'],headers=flipkart_headers,callback=self.parse_products_url)
    
    def closed(self,reason):
        s_file=open(reviews_seed_file.format(categoryId=self.categoryId),'w')
        s_file.write(json.dumps(self.product_urls))
        s_file.close()
        print reason