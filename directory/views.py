from django.shortcuts import render
from django.http import HttpResponse
from directory.models import Person, Page, User, Category
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
import json
from urllib.request import urlopen
import urllib.request
import urllib

def index(request):
	if request.user.is_authenticated():
		friend_list=Person.objects.filter(user=request.user).order_by('rank')
		page_list=Page.objects.filter(person=friend_list).order_by('-created_at')

	else:
		friend_list=Person.objects.order_by('rank')
		page_list=None
	
	context_dict = {'Friends': friend_list, 'Page':page_list, }
	
	return render(request, 'directory/index.html', context=context_dict)

def home(request):

	profile = user.get_profile()
	if profile is None:
		profile = Profile(user_id=user.id)
		print(profile)
		gender = response.get('gender')
		print(gender)
	friend_list=Person.objects.filter(user=request.user).order_by('rank')
	page_list=Page.objects.order_by('-created_at')
	context_dict = {'Friends': friend_list, 'Page':page_list, 'gender':gender, 'profile':profile}
	
	return render(request, 'directory/home.html', context=context_dict)

def about(request):
	context_dict ={'yourname': "Nicky Collins"}
	return render(request, 'directory/about.html', context=context_dict)

def show_person(request, person_name_slug, username):
	context_dict = {}
	user = User.objects.get(username=username)
	try: 
		person = Person.objects.filter(user=request.user).get(slug=person_name_slug)
		pages = Page.objects.filter(person=person)
		category=Category.objects.all()
		context_dict['pages']=pages
		context_dict['person']=person
		context_dict['category']=category
	except Person.DoesNotExist:
		context_dict['person'] = None
		context_dict['pages']=None

	return render(request, 'directory/person.html', context_dict)

def select_category(request, person_name_slug, username):
	user = User.objects.get(username=username)
	context_dict = {}
	try:
		category=Category.objects.all()
		person = Person.objects.filter(user=request.user).get(slug=person_name_slug)
		context_dict['person']=person
		context_dict['category']=category
	except Person.DoesNotExist:
		context_dict['person']=None
		context_dict['category']=category

	return render(request, 'directory/select_category.html', context_dict)

def show_category(request, person_name_slug, categoryid, username):
	user = User.objects.get(username=username)
	try:
		person=Person.objects.get(slug=person_name_slug)
		category1=Category.objects.get(categoryid=categoryid)

	except Person.DoesNotExist:
		person=None

	form=PageForm()

	if request.method =='POST':
		form=PageForm(request.POST)

		if form.is_valid():
			if person:	
				page=form.save(commit=False)
				page.category=category1
				page.person=person
				page.views=0
				page.save()
				return show_person(request, person_name_slug, username)
		else:
			print (form.errors)
	context_dict ={'form':form, 'person':person, 'category':category1}
	return render(request, 'directory/show_category.html', context_dict)


def show_page(request, person_name_slug, pageid, username):
	user = User.objects.get(username=username)
	context_dict = {}

	try: 
		p1 = Page.objects.get(id=pageid)

	
		context_dict['p1']=p1

	except Page.DoesNotExist:
		print("no page")
		context_dict['p1']=None

	return render(request, 'directory/page.html', context_dict)


def add_person(request, ):
	
	form=PersonForm()

	if request.method =='POST':
		form=PersonForm(request.POST)

		# only if form is valid

		if form.is_valid():
			cat=form.save(commit=False)
			cat.user=request.user
			cat.save()
			print("Added Person with name:", cat, "and slug", cat.slug)
			return index(request)
		else:
			print(form.errors)
	return render(request, 'directory/add_person.html', {'form':form})


def add_page(request, person_name_slug, username):
	user = User.objects.get(username=username)
	try:
		person=Person.objects.filter(user=request.user).get(slug=person_name_slug)
		category=Category.objects.all()
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
				return show_person(request, person_name_slug, username)
		else:
			print (form.errors)
	context_dict ={'form':form, 'person':person}
	return render(request, 'directory/add_page.html', context_dict)


def delete(request, person_name_slug, pageid, username):
	user = User.objects.get(username=username)
	query = Page.objects.get(pk=pageid)
	query.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'query':query})


def edit_page(request, person_name_slug, pageid, username):
	user = User.objects.get(username=username)
    
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

def email(request, person_name_slug, username):
	user = User.objects.get(username=username)
	person = Person.objects.filter(user=request.user).get(slug=person_name_slug)
	p1 = Page.objects.filter(person=person).order_by('-created_at')[:2]
	address=None
	email=["njcollins5@gmail.com"]
	if request.user.is_authenticated():
		address=request.user.email
		email.append(address)
	subject = "Updates from Friends Directory"
	to = email
	from_email = 'njcollins5@gmail.com'
	

	context_dict = {}

	try: 
		person = Person.objects.filter(user=request.user).get(slug=person_name_slug)
		pages = Page.objects.filter(person=person).order_by('-created_at')[:2]
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




def Facebook(request,):
	social_user = request.user.social_auth.filter(
	    provider='facebook',
	).first()
	if social_user:
	    url = u'https://graph.facebook.com/{0}/' \
	          u'friends?fields=email,id,name,location,picture' \
	          u'&access_token={1}'.format(
	              social_user.uid,
	              social_user.extra_data['access_token'],
	          )
	    response = urllib.request.urlopen(url).read().decode('utf8')
	    data = json.loads(response)
	    print(data)
	return render(request, 'directory/facebook.html', {'data':data})
import httplib2
from allauth.socialaccount.models import SocialToken
def Google(request):
    nicky=request.user
    access_token = SocialToken.objects.filter(account__user=request.user, account__provider='google')
 
    ''' 
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])'''
    return render(request, 'directory/google.html', {'access_token':access_token, 'nicky':nicky})
           