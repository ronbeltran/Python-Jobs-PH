
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic import list_detail
from django.conf.urls.defaults import *

from jobs.models import Entry, Category, Company
from jobs.views import limited_object_list, limited_object_detail

entry_info_dict = {
    'queryset': Entry.live.all(),
    'template_object_name':'entry',
}

category_info_dict = {
    'queryset': Category.objects.all(),
}

company_info_dict = {
    'queryset': Company.objects.all(),
    'template_object_name':'entry',
}

urlpatterns = patterns('',
    # jobs index
    url(r'^$', 'jobs.views.index_redirect', name='index_redirect'),
    # edit job
    url(r'^edit/job/(?P<object_id>\d+)/$', 'jobs.views.edit_job', name='edit_job'),
    # edit company 
    url(r'^edit/company/(?P<object_id>\d+)/$', 'jobs.views.edit_company', name='edit_company'),
    # preview entry with draft and expired status
    url(r'^preview/(?P<object_id>\d+)/$', limited_object_detail,
        {'queryset':Entry.objects.exclude(status=Entry.LIVE_STATUS), 'template_object_name':'entry', 'template_name':'jobs/entry_preview_detail.html',},
        name="job_preview_detail"),
    
    url(r'^category/(?P<slug>[-\w]+)/$', 'jobs.views.category_detail', name="job_category_detail"),
    url(r'^companies/$', list_detail.object_list, company_info_dict, name="job_company_list"),
    url(r'^companies/(?P<slug>[-\w]+)/(?P<object_id>\d+)/$',
        list_detail.object_detail,
        company_info_dict, name="job_company_detail"),
    url(r'^post/job/$', 'jobs.views.post_job', name="post_job"),
    url(r'^post/company/$', 'jobs.views.post_company', name="post_company"),
    # view job entry detail
    url(r'^(?P<slug>[-\w]+)/(?P<object_id>\d+)/$', list_detail.object_detail,
        entry_info_dict, name="job_entry_detail"),

)

