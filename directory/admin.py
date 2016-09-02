from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from directory.models import Person, Page, UserProfile, Category


# Register your models here.
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
	list_display=('name',)
class PageAdmin(admin.ModelAdmin):
	list_display=('title',)
class PersonAdmin(admin.ModelAdmin):
	#code to display multiple columns in admin table
	list_display = ('name', 'rank',)
	#code to prepopulate the slug field when you type in a new category name
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(UserProfile)