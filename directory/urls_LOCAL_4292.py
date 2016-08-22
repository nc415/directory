from django.conf.urls import url
from directory import views
from directory.views import UpdateView

urlpatterns =[
	url(r'^$', views.index, name='index'),
	url(r'^about$', views.about, name='about'),
	url(r'^add_person$', views.add_person, name='add_person'),
	url(r'^person/(?P<person_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
#n [\w\-]+) will look
#for any sequence of alphanumeric characters e.g. a-z, A-Z, or 0-9 denoted by \w and any hyphens
#(-) denoted by \-, and we can match as many of these as we like denoted by the [ ]+ expression.
	url(r'^person/"(?P<person_name_slug>[\w\-]+)"/$', views.show_person, name='show_person'),
	url(r'^person/(?P<person_name_slug>[\w\-]+)/$', views.show_person, name='show_person'),
	url(r'^person/(?P<person_name_slug>[\w\-]+)/(?P<pageid>[\w\-]+)$', views.show_page, name='show_page'),
	url(r'^person/(?P<person_name_slug>[\w\-]+)/(?P<pageid>[\w\-]+)/delete$', views.delete, name='delete-person'),
	url(r'^person/(?P<person_name_slug>[\w\-]+)/(?P<pageid>[\w\-]+)/edit$', views.edit_page, name='delete-person'),
	url(r'^person/(?P<person_name_slug>[\w\-]+)/email', views.email , name = 'sendSimpleEmail'),
	

]

'''	url(r'^register/', views.register , name = 'register'),
	url(r'^login/', views.user_login , name = 'login'),
	url(r'^logout/$', views.user_logout, name='logout'),'''