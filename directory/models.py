from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime
# Create your models here.
class Person(models.Model):
	name=models.CharField(max_length=128, unique=True)
	description=models.CharField(max_length=200)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	date = models.DateTimeField(default=datetime.now, blank=True, null=True)
# Define as slug to use as the URL
	slug = models.SlugField(blank=True, unique=True)

# override default save to allow for the saving of the name with slugify filter
# This filter removes the spaces in multiple word sentences e.g. hello world becomes hello-world

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Person, self).save(*args, **kwargs)
# Fix issue where the plural of category is categories NOT categorys
	def __str__(self):
			return self.name

class Page(models.Model):
	person = models.ForeignKey(Person)
	title = models.CharField(max_length=128, unique=True)
	description=models.CharField(null=True, blank=True, max_length=2000)
	page_slug = models.SlugField(blank=True, unique=True)
	created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)


# override default save to allow for the saving of the name with slugify filter
# This filter removes the spaces in multiple word sentences e.g. hello world becomes hello-world

	def save(self, *args, **kwargs):
		self.page_slug = slugify(self.title)
		super(Page, self).save(*args, **kwargs)

	def __str__(self):
		return self.title
