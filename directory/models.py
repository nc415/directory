from django.db import models
from django.conf.urls import patterns, include, url
from django.template.defaultfilters import slugify
from datetime import datetime
from django.contrib.auth.models import User
import random
import string
from django.core.exceptions import ValidationError
# Create your models here.

class UserProfile(models.Model):
	user=models.OneToOneField(User)
	website=models.URLField(blank=True)
	picture=models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.user.username

class Person(models.Model):
	user=models.ForeignKey(User)
	
	CLASSIFICATION_CHOICES= (
        ('F', 'Friend'),
        ('C', 'Colleague'),
        ('L', 'Client'),
    )
	classification=models.CharField(max_length=128, choices=CLASSIFICATION_CHOICES)

	name=models.CharField(max_length=128, unique=False)
	
	rank=models.IntegerField(null=True, unique=False)
	# Define as slug to use as the URL
	slug = models.SlugField(blank=True, unique=True)
	profile_picture=models.URLField(blank=True, unique=False)
	FB_link=models.URLField(blank=True, unique=False)
	
	#contact
	contact_email=models.EmailField(blank=True, unique=False)
	contact_number=models.IntegerField(blank=True, unique=False, default=0)
	

	#personal
	mum_name=models.CharField(max_length=128, blank=True, unique=False)
	dad_name=models.CharField(max_length=128, blank=True, unique=False)
	sibling_names=models.CharField(max_length=128, blank=True, unique=False)
	partner_name=models.CharField(max_length=128, blank=True, unique=False)





	def save(self, *args, **kwargs):
		s=random.randint(0,100)
		name=str(self.name)
		user=str(self.user)
		nameslug = slugify(name)
		userslug=slugify(user)
		self.slug=userslug+"-"+nameslug
		
		super(Person, self).save(*args, **kwargs)

# Fix issue where the plural of category is categories NOT categorys
	def __str__(self):
			return self.name



class Category(models.Model):
	name=models.CharField(max_length=128, unique=True)
	categoryid = models.SlugField(blank=True, unique=True, default=0)
	def __str__(self):
		return self.name

class Page(models.Model):
	
	person = models.ForeignKey(Person)
	category = models.ForeignKey(Category, default=0)
	title = models.CharField(max_length=128, null=False)
	description=models.CharField(null=True, blank=True, max_length=2000)
	pageid = models.SlugField(blank=True, unique=False)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	

		

	def get_absolute_url(self):
		return reverse('page-title', kwargs={'pk': self.pk})


# override default save to allow for the saving of the name with slugify filter
# This filter removes the spaces in multiple word sentences e.g. hello world becomes hello-world
    

	def save(self, *args, **kwargs):
		self.page_slug = slugify(self.title)
		super(Page, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

