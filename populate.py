import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Friend.settings')

import django
django.setup()
from directory.models import Page, Person
from datetime import datetime
import csv 

with open('friendlist.csv', 'rb') as csvfile:
	friendreader=csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in friendreader:
		row[0].decode('utf-8')
		row[1].decode('utf-8')
		print (row[0])

		def populate():

			person1 = add_person(name=row[0], description=row[1])
			

		def add_person(name, description):
			c=Person.objects.get_or_create(name=name, description=description)[0]
			return c

		def add_page(person, title):
			p=Page.objects.get_or_create(title=title, person=person)[0]
			return p

		if __name__ == '__main__':
			print("Starting population script")
			populate()
