import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Friend.settings')

import django
django.setup()
from directory.models import Page, Person, Category
from datetime import datetime
import csv 


def populate():

	category = add_category(name)
	

def add_category(name):
	name=['Other', 'Personal']
	c=Category.objects.get_or_create(name=name)[0]
	return c


if __name__ == '__main__':
	print("Starting population script")
	populate()
