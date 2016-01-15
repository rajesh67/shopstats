# -*- coding: utf-8 -*-

import scrapy
import json
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapper.models import FlipkartReview,FlipkartBaseProduct,Image
from shopstatsbot.items import ReviewItem
#from scrapperdata.flipkart.models import FlipkartBaseProduct

from urlparse import urlparse,parse_qs
import re
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

flipkart_affid='rajeshmee'
flipkart_token='78fef03fe9d84c9eb6387b80ba4c98d2'
flipkart_headers={'Fk-Affiliate-Id':flipkart_affid,'Fk-Affiliate-Token':flipkart_token}
flipkart_categories=["tablets","mobiles","laptops","cameras","desktops","laptops"]
reviews_seed_file='flipkart.{categoryId}.reviews.seeds.txt'

class FlipkartSpider(scrapy.Spider):
    name = "flipkart_products_api"
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
        if 'nextUrl' in products_data.keys():
            nextUrl=products_data['nextUrl']
            if nextUrl:
                request=scrapy.Request(url=nextUrl,headers=flipkart_headers,callback=self.parse_category)
                request.meta['categoryId']=categoryId
                yield request
        product_list=products_data['productInfoList']
        for product in product_list:
            identifiers=product['productBaseInfo']['productIdentifier']
            attributes=product['productBaseInfo']['productAttributes']
            productId=identifiers['productId']
            categoryPaths=identifiers['categoryPaths']
            #print attributes
            product,created=FlipkartBaseProduct.objects.get_or_create(productId=productId)
            if created:
                product.title=attributes['title']
                product.categories=categoryPaths
                product.productUrl=attributes['productUrl']
                product.brand=attributes['productBrand']
                product.description=attributes['productDescription']
                colorVariants=attributes['colorVariants']
                if colorVariants:
                    product.colorVariants=list(colorVariants)
                color=attributes['color']
                if color:
                    product.color=attributes['color']
                codAvailable=attributes['codAvailable']
                if codAvailable:
                    product.codAvailable=codAvailable
                emiAvailable=attributes['emiAvailable']
                if emiAvailable:
                    product.emiAvailable=emiAvailable
                styleCode=attributes['styleCode']
                if styleCode:
                    product.styleCode=styleCode
                offers=attributes['offers']
                if offers:
                    product.offers=offers
                discount=attributes['discountPercentage']
                if discount:
                    product.discount=discount
                inStock=attributes['inStock']
                if inStock:
                    product.inStock=inStock
                retailPrice=attributes['maximumRetailPrice']['amount']
                if retailPrice:
                    product.retailPrice=retailPrice
                cashback=attributes['cashBack']
                if cashback:
                    product.cashback=cashback
                size=attributes['size']
                if size:
                    product.size=size
                sizeVariants=attributes['sizeVariants']
                if sizeVariants:
                    product.sizeVariants=list(sizeVariants)
                sizeUnit=attributes['sizeUnit']
                if sizeUnit:
                    product.sizeUnit=sizeUnit
                sellingPrice=attributes['sellingPrice']['amount']
                if sellingPrice:
                    product.sellingPrice=sellingPrice
                imageUrls=attributes['imageUrls']
                if imageUrls:
                    for key,url in imageUrls.iteritems():
                        image=Image(size=key,url=url)
                        product.images.append(image)
                product.save()
            else:
                print "product Already Available and product title=%s"%product.title

#flipkart reviews processor
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
        self.reviewId=''

    def __dict__(self):
        return {
            'reviewId':self.reviewId,
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
                    #span.review-username is also available please add
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
                    if certified=='certified buyer':
                        review.certified_buyer=True
                except Exception, e:
                    review.certified_buyer=False
                try:
                    first_review=review_box.css('img.firstReviewerBadge::attr(alt)').extract()[0]
                    if first_review=='First to review':
                        review.first_review=True
                    if first_review=='first to review':
                        review.first_review=True
                except Exception, e:
                    review.first_review=False
                    #print "Couldn't get certificate of reviewer"

            def _review_rating():
                try:
                    rating=review_box.css('div.fk-stars::attr(title)').extract()[0]
                    rating=re.search('\d+',rating).group()
                    print rating
                    review.rating=locale.atoi(rating)
                except Exception, e:
                    print "Couldn't get rating for this reviewer %s"%review.reviewer
            
            def _review_parmalink():
                review.reviewId=review_box.css('::attr(review-id)').extract()[0]
                try:
                    url=review_box.css('div.unitExt>a::attr(href)').extract()[0]
                    review.parmalink=_normalize_url(url)
                except Exception, e:
                    review.parmalink='http://www.flipkart.com/reviews/%s'%review.reviewId
                    if not review.reviewId:
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
            review.productId=response.url.split('?')[-1].split('&')[0].replace('pid=','')
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
        processor=FlipkartReviewsProcessor()
        reviews=processor.process_response(response)
        for review in reviews:
            item=ReviewItem()
            reviewId=review['reviewId']
            productId=review['productId']
            reviewer=review['reviewer']
            reviewer_url=review['reviewer_url']
            certified=review['certified']
            date=review['date']
            head=review['head']
            parmalink=review['parmalink']
            review_text=review['review_text']
            rating=review['rating']
            
            item['reviewId']=reviewId
            item['productId']=productId
            item['reviewer']=reviewer
            item['reviewer_url']=reviewer_url
            item['certified']=certified
            item['date']=date
            item['head']=head
            item['parmalink']=parmalink
            item['review_text']=review_text
            item['rating']=rating
            yield item
            
            flipkart_review,created=FlipkartReview.objects.get_or_create(reviewId=reviewId)
            if created:
                flipkart_review.reviewId=reviewId
                flipkart_review.productId=productId
                flipkart_review.parmalink=parmalink
                flipkart_review.head=head
                flipkart_review.text=review_text
                flipkart_review.posted_on=date
                flipkart_review.username=reviewer
                flipkart_review.userprofile=reviewer_url
                flipkart_review.rating=rating
                flipkart_review.certified=certified
                flipkart_review.save()
            else:
                print "Review already available"
                  
    def filter_links(self,links):
        for link in links:
            if link not in self.reviews_url:
                self.reviews_url.append(link)
        return self.reviews_url
    
    def parse_start_url(self,response):
        processor=FlipkartReviewsProcessor()
        reviews=processor.process_response(response)
        for review in reviews:
            item=ReviewItem()
            reviewId=review['reviewId']
            productId=review['productId']
            reviewer=review['reviewer']
            reviewer_url=review['reviewer_url']
            certified=review['certified']
            date=review['date']
            head=review['head']
            parmalink=review['parmalink']
            review_text=review['review_text']
            rating=review['rating']
            
            item['reviewId']=reviewId
            item['productId']=productId
            item['reviewer']=reviewer
            item['reviewer_url']=reviewer_url
            item['certified']=certified
            item['date']=date
            item['head']=head
            item['parmalink']=parmalink
            item['review_text']=review_text
            item['rating']=rating
            yield item
            
            flipkart_review,created=FlipkartReview.objects.get_or_create(reviewId=reviewId)
            if created:
                flipkart_review.reviewId=reviewId
                flipkart_review.productId=productId
                flipkart_review.parmalink=parmalink
                flipkart_review.head=head
                flipkart_review.text=review_text
                flipkart_review.posted_on=date
                flipkart_review.username=reviewer
                flipkart_review.userprofile=reviewer_url
                flipkart_review.rating=rating
                flipkart_review.certified=certified
                flipkart_review.save()
            else:
                print "Review already available"

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
        #self.close()