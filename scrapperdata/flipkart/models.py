from django.db import models
from djangotoolbox.fields import EmbeddedModelField,ListField
# Create your models here.

class Image(EmbeddedModelField):
	url=models.URLField(max_length=300)

class FlipkartBaseProduct(models.Model):
	categories=models.CharField(max_length=50)
	productId=models.CharField(max_length=20)
	productUrl=models.URLField(max_length=300)
	
	title=models.CharField(max_length=100)
	brand=models.CharField(max_length=30)
	description=models.TextField()
	colorVariants=ListField()
	color=models.CharField(max_length=20)
	codAvailable=models.BooleanField(default=False)
	emiAvailable=models.BooleanField(default=False)
	styleCode=models.CharField(max_length=30)
	offers=models.TextField()

	discount=models.FloatField(default=0.0)
	inStock=models.BooleanField(default=False)
	retailPrice=models.PositiveIntegerField(default=0)
	sellingPrice=models.PositiveIntegerField(default=0)
	cashback=models.CharField(max_length=10)
	size=models.CharField(max_length=10)
	sizeVarients=ListField()
	sizeUnit=models.CharField(max_length=10)
	images=ListField(EmbeddedModelField(Image))

class FlipkartReview(models.Model):
	reviewId=models.CharField(max_length=30)



