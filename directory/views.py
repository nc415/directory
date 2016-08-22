from django.shortcuts import render
from django.http import HttpResponse
from directory.models import Person, Page, User
from directory.forms import PersonForm,PageForm, UserProfileForm, UserForm, EditPageForm
from django.db.models import manager

from django.conf.urls import patterns, include, url
from django.utils import timezone
from django.shortcuts import redirect
from django import forms
from django.shortcuts import get_object_or_404
import re
from django.views.generic.edit import UpdateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.http import HttpResponseRedirect
from django.core.exceptions import MultipleObjectsReturned
def index(request):
	friend_list=Person.objects.order_by('rank')
	context_dict = {'Friends': friend_list}

	return render(request, 'directory/index.html', context=context_dict)


def about(request):
	context_dict ={'yourname': "Nicky Collins"}
	return render(request, 'directory/about.html', context=context_dict)

def show_person(request, person_name_slug):
	context_dict = {}

	try: 
		person = Person.objects.get(slug=person_name_slug)
		pages = Page.objects.filter(person=person)
		context_dict['pages']=pages
		context_dict['person']=person
	except Person.DoesNotExist:
		context_dict['person'] = None
		context_dict['pages']=None

	return render(request, 'directory/person.html', context_dict)





def show_page(request, person_name_slug, pageid):
	context_dict = {}

	try: 
		p1 = Page.objects.get(id=pageid)

	
		context_dict['p1']=p1

	except Page.DoesNotExist:
		print("no page")
		context_dict['p1']=None

	return render(request, 'directory/page.html', context_dict)


def add_person(request):
	form=PersonForm()

	if request.method =='POST':
		form=PersonForm(request.POST)

		# only if form is valid

		if form.is_valid():
			cat=form.save(commit=True)
			print("Added Person with name:", cat, "and slug", cat.slug)
			return index(request)
		else:
			print(form.errors)
	return render(request, 'directory/add_person.html', {'form':form})


def add_page(request, person_name_slug):
	try:
		person=Person.objects.get(slug=person_name_slug)
	except Person.DoesNotExist:
		person=None
	form=PageForm()

	if request.method =='POST':
		form=PageForm(request.POST)

		if form.is_valid():
			if person:	
				page=form.save(commit=False)
				page.person=person
				page.views=0
				page.save()
				return show_person(request, person_name_slug)
		else:
			print (form.errors)
	context_dict ={'form':form, 'person':person}
	return render(request, 'directory/add_page.html', context_dict)


def delete(request, person_name_slug, pageid):
    query = Page.objects.get(pk=pageid)
    query.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'query':query})


def edit_page(request, person_name_slug, pageid):
    
	query=Page.objects.get(pk=pageid)
	
	person=Person.objects.get(slug=person_name_slug)
	form=EditPageForm(instance=query)
	
	if request.method=='POST':
		form = EditPageForm(request.POST, instance=pageid)
		random=form.data['created_at']

		if form.is_valid():
			if person:	
				page=form.save(commit=False)
				page.created_at=random
				page.person=person
				page.save(instance=pageid)

	query.delete()
	
	context_dict ={'form':form, 'person':person}
	return render(request, 'directory/edit_page.html', context_dict)

def email(request, person_name_slug):
	person = Person.objects.get(slug=person_name_slug)
	p1 = Page.objects.filter(person=person)
	address=None
	email=[]
	if request.user.is_authenticated():
		address=request.user.email
		email.append(address)
	subject = "Updates from Friends Directory"
	to = email
	from_email = 'njcollins5@gmail.com'
	

	context_dict = {}

	try: 
		person = Person.objects.get(slug=person_name_slug)
		pages = Page.objects.filter(person=person).order_by('created_at')[:2]
		context_dict['pages']=pages
		context_dict['person']=person
	except Person.DoesNotExist:
		context_dict['person'] = None
		context_dict['pages']=None



	message = get_template('email/Test.html').render(Context(context_dict))
	msg = EmailMessage(subject, message, to=to, from_email=from_email)
	msg.content_subtype = 'html'
	msg.send()
	return render(request, 'directory/email.html', {'person':person, 'pages':pages, 'address':address}, )



	'''email = EmailMessage('Subject', 'Body', to=['njcollins@live.co.uk'])
	email.send()
	return render(request, 'directory/page.html')'''
