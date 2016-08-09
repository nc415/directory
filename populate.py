import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Friend.settings')

import django
django.setup()
from directory.models import Page, Person
from datetime import datetime

def populate():

	person1 = add_person(name="Nicky Collins", description="Family")
	person2 = add_person(name="Emma Collins", description="Family")
	person3 = add_person(name="Carolyn Collins", description="Family")
	person4 = add_person(name="Paul Collins", description="Family")

	detail1 = add_page(person=person1, title="Default Page")
	detail2 = add_page(person=person2, title="Default Page")
	detail3 = add_page(person=person3, title="Default Page")
	detail4 = add_page(person=person4, title="Default Page")

def add_person(name, description):
	c=Person.objects.get_or_create(name=name, description=description)[0]
	return c

def add_page(person, title):
	p=Page.objects.get_or_create(title=title, person=person)[0]
	return p

if __name__ == '__main__':
	print("Starting population script")
	populate()
