from django.db import models
from djangotoolbox.fields import EmbeddedModelField,ListField
# Create your models here.
from datetime import datetime

class Image(models.Model):
	size=models.CharField(max_length=30)
	url=models.URLField(max_length=300)

class FlipkartBaseProduct(models.Model):
	categories=models.CharField(max_length=100)
	productId=models.CharField(max_length=20)
	productUrl=models.URLField(max_length=300)
	
	title=models.CharField(max_length=100)
	brand=models.CharField(max_length=30)
	description=models.TextField(null=True)
	colorVariants=ListField()
	color=models.CharField(max_length=20)
	codAvailable=models.BooleanField(default=False)
	emiAvailable=models.BooleanField(default=False)
	styleCode=models.CharField(max_length=30)
	offers=models.TextField()

	discount=models.FloatField(default=0.0)
	inStock=models.BooleanField(default=False)
	retailPrice=models.FloatField(default=0.0)
	sellingPrice=models.FloatField(default=0.0)
	cashback=models.CharField(max_length=10)
	size=models.CharField(max_length=10)
	sizeVarients=ListField()
	sizeUnit=models.CharField(max_length=10)
	images=ListField(EmbeddedModelField('Image'))

class SnapdealBaseProduct(models.Model):
	url=models.URLField(max_length=300)

class FlipkartProduct(FlipkartBaseProduct):
	pass

class FlipkartReview(models.Model):
	reviewId=models.CharField(max_length=30)
	productId=models.CharField(max_length=30)
	parmalink=models.URLField(max_length=200)

	head=models.CharField(max_length=200)
	text=models.TextField()
	posted_on=models.CharField(default=False)
	username=models.CharField(max_length=50)
	userprofile=models.URLField(max_length=300)
	rating=models.PositiveIntegerField(default=0)
	certified=models.BooleanField(default=False)	


class SnapdealReview(models.Model):
	productId=models.CharField(max_length=30)
	reviewId=models.CharField(max_length=50)
	date=models.CharField(max_length=30)
	head=models.CharField(max_length=500)
	text=models.TextField()
	rating=models.PositiveIntegerField(default=0)
	username=models.CharField(max_length=64)
	certified=models.BooleanField(default=False)