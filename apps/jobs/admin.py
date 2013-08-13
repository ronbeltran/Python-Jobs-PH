from django.forms import Textarea, TextInput
from django.db import models
from django.contrib import admin

from tinymce.widgets import TinyMCE
from jobs.models import Company, Category, Entry

class CategoryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': TinyMCE(attrs={'cols': 100, 'rows': 20})},
    }
    prepopulated_fields = { 'slug': ['title'] }
    list_display = ('title','description_html','slug', 'pub_date',)
    ordering = ('title',)

class CompanyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.URLField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': TinyMCE(attrs={'cols': 100, 'rows': 20})},
    }
    prepopulated_fields = { 'slug': ['name'] }
    list_display = ('name','slug','address','telephone','fax','email','url','pub_date',)
    ordering = ('name',)

class EntryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': TinyMCE(attrs={'cols': 100, 'rows': 20})},
    }

    prepopulated_fields = { 'slug': ['job_title'] }
    list_display = ('job_title','author','status','slug','pub_date',)
    #list_display = ('job_title','author','status','type','slug','pub_date',)
    ordering = ('status','pub_date')
    list_filter = ('status','pub_date')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Entry, EntryAdmin)
