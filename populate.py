import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Friend.settings')

import django
django.setup()
from directory.models import Page, Person
from datetime import datetime
import csv 

with open('friendlist.csv', 'r') as csvfile:
	friendreader=csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in friendreader:
		
		print (row[0])

		def populate():

			person1 = add_person(name=row[0], rank=row[1] )
			

		def add_person(name, rank):
			
			c=Person.objects.get_or_create(name=name, rank=rank, user_id=21)[0]
			return c

		def add_page(person, title):
			p=Page.objects.get_or_create(title=title, person=person)[0]
			return p

		if __name__ == '__main__':
			print("Starting population script")
			populate()
