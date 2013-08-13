
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic import list_detail
from django.conf.urls.defaults import *

from posts.models import Entry, Category

entry_info_dict = {
    'queryset': Entry.live.all(),
#    'template_object_name':'posts',
}

category_info_dict = {
    'queryset': Category.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', list_detail.object_list, entry_info_dict, name="post_list"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$', 'posts.views.entry_detail', name='entry_detail',),
    url(r'^preview/$', 'posts.views.preview_list', name='preview_list',),
    url(r'^category/(?P<slug>[-\w]+)/$', 'posts.views.category_detail', name='category_detail',),
)

