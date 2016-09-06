from django import forms
from directory.models import Page, Person, UserProfile
from datetime import datetime
from django.db.models import Q
import itertools
from django.utils.text import slugify
from django.contrib.auth.models import User
class PersonForm(forms.ModelForm):

	name = forms.CharField(max_length=128, help_text="please enter a person name.")
	#HiddenInput with an intial equal to 0 is essentially a way to set the default to 0
	#We then dont include these fields when we define what to include in the class Meta:
	user=forms.CharField(widget=forms.HiddenInput(),required=False )
	slug=forms.CharField(widget=forms.HiddenInput(), required=False)

	# provides additional information on form such as the link between the form
	# and which model to use from Models.py, in this case, Category model
	class Meta:
		model = Person
		exclude =('slug', 'rank', 'user')

class PageForm(forms.ModelForm):
	title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Page Title'}), max_length=128)
	description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Description'}), max_length=2000)
	# we have to include this next line because in our model, views doesnt have a default value
	
	created_at=forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.now)
	#in case the user failed to enter a URL in the correct format, i.e. with http://
	pageid=forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)

	class Meta:
		model = Page
		#what fields to include in the form? In our model we have "category"
		#as a field, but we dont want to include this, so specify what to include
		exclude =('person','pageid','created_at' )
		abstract=True


class EditPageForm(forms.ModelForm):
	title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Page Title'}), max_length=128)
	description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Description'}), max_length=2000)
	# we have to include this next line because in our model, views doesnt have a default value
	
	created_at=forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.now)
	#in case the user failed to enter a URL in the correct format, i.e. with http://
	pageid=forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)

	class Meta:
		model = Page
		#what fields to include in the form? In our model we have "category"
		#as a field, but we dont want to include this, so specify what to include
		exclude =('person','pageid','created_at' )
		abstract=True

	
class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture')
        