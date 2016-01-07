from django.db import models

# Create your models here.
from django.db import models
from djangotoolbox.fields import ListField
# Create your models here.

class FlipkartProduct(models.Model):

	store=models.CharField(max_length=50,null=True)
	categoryId=models.CharField(max_length=50,null=True)

	product_id=models.CharField(max_length=30)
	product_title=models.CharField(max_length=200)
	product_url=models.CharField(max_length=300)
	
	description=models.TextField()
	#categories information

	categories=models.CharField(max_length=50)
	
	#price and cashback information
	price=models.FloatField(default=0.0)
	mrp=models.FloatField(default=0.0)
	discount=models.FloatField(default=0.0)
	cashback=models.FloatField(default=0.0)
	offers=models.CharField(max_length=200)
	
	#color and varients information
	color=models.CharField(max_length=30)
	color_varients=ListField()
	size=models.CharField(max_length=30)
	sizeunit=models.CharField(max_length=30)
	size_varients=ListField()
	stylecode=models.CharField(max_length=30)

	#stock and images information
	images=ListField()
	instock=models.BooleanField(default=True)
	brand=models.CharField(max_length=50)
	delivery_time=models.CharField(max_length=200)
	emi_available=models.BooleanField(default=False)
	cod_available=models.BooleanField(default=False)

	total_reviews=models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return self.product_title
