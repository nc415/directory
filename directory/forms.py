from django import forms
from directory.models import Page, Person
from datetime import datetime

class PersonForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="please enter a person name.")
	#HiddenInput with an intial equal to 0 is essentially a way to set the default to 0
	#We then dont include these fields when we define what to include in the class Meta:
	views= forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug=forms.CharField(widget=forms.HiddenInput(), required=False)

	# provides additional information on form such as the link between the form
	# and which model to use from Models.py, in this case, Category model
	class Meta:
		model = Person
		fields =('name',)

class PageForm(forms.ModelForm):
	title=forms.CharField(max_length=128, help_text="Please enter title of the page.")
	description = forms.CharField(max_length=2000, help_text="Please enter the Description")
	# we have to include this next line because in our model, views doesnt have a default value
	
	created_at=forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.now)
	#in case the user failed to enter a URL in the correct format, i.e. with http://
	page_slug=forms.CharField(widget=forms.HiddenInput(), initial=0, required=False)

	class Meta:
		model = Page
		#what fields to include in the form? In our model we have "category"
		#as a field, but we dont want to include this, so specify what to include
		exclude =('person','page_slug', 'created_at')
		abstract=True

