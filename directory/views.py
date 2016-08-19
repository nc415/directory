from django.shortcuts import render
from django.http import HttpResponse
from directory.models import Person, Page
from directory.forms import PersonForm,PageForm, UserProfileForm, UserForm
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
from django.core.mail import send_mail

def edit_page(request):
	model=PageForm
	fields=['title']

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

def update_page(request, person_name_slug, page_title_slug, pk=None):

    obj = get_object_or_404(Page, pk=pk)
    form = PageForm(request.POST or None,
                        request.FILES or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
           form.save()
           return redirect('/')
    return render(request, 'directory/edit_page.html', {'form': form})

class UpdateView(UpdateView,):
	slug='page_title_slug'
	model=Page
	template_name='edit_page.html'
	form_class=PageForm
	success_url = '/'


def delete(request, person_name_slug, pageid):
    query = Page.objects.get(pk=pageid)
    query.delete()
    return render(request, 'directory/deleted.html', {'query':query})


from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

def email(request, pageid, person_name_slug):

	identity=Page.objects.get(pk=pageid)
	subject = "Page update"
	to = ['njcollins5@gmail.com']
	from_email = 'njcollins@live.co.uk'
	message = get_template('directory/email.html')
	msg=EmailMessage(subject, message, to=to, from_email=from_email)
	msg.content_subtype ='html'
	msg.send()

	return HttpResponse('email_two')

'''old Login System
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/directory/')

def user_login(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/directory/')
			else:
				return HttpResponse("Your account is disabled")
		else:
			print ("Invalid Login Details:{0}, {1}".format(username,password))
			return HttpResponse("Invalid login Details Supplied.")
	else:
		return render(request, 'directory/login.html', {})

def register(request):
	registered=False
	if request.method =='POST':
		user_form=UserForm(data=request.POST)
		profile_form=UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()

			user.set_password(user.password)
			user.save()

			profile=profile_form.save(commit=False)
			profile.user=user

			if 'picture' in request.FILES:
				profile.picture=request.FILES['picture']

			profile.save()
			registered=True
		else:
			print (user_form.errors, profile_form.errors)
	else:
		user_form=UserForm()
		profile_form=UserProfileForm()

	return render(request, 'directory/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})
'''