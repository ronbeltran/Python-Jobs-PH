
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail

handler500 = 'djangotoolbox.errorviews.server_error'

# Django Admin
from django.contrib import admin
admin.autodiscover()

# Search for "dbindexes.py" in all installed apps
import dbindexer
dbindexer.autodiscover()

# Search for "search_indexes.py" in all installed apps
import search
search.autodiscover()

from accounts.forms import UserProfileForm
from jobs.models import Entry, Category, Company

from jobs.feeds import LatestJobsFeed, LatestCompaniesFeed
from jobs.sitemap import EntrySitemap, CategorySitemap, CompanySitemap

feeds = {
    'jobs': LatestJobsFeed,
    'companies': LatestCompaniesFeed,
}

sitemaps = {
    'jobs': EntrySitemap,
    'categories': CategorySitemap,
    'companies': CompanySitemap,
}


urlpatterns = patterns('',

    url(r'^$', 'views.home_page', name='home_page',),
    url(r'^about/$', direct_to_template,{ 'template':'about.html',}, name='about_page',),
    url(r'^about/faq/$', direct_to_template,{ 'template':'faq.html',}, name='faq_page',),

    # Jobs
    (r'^v/', include('jobs.urls')),

    # Blog 
    (r'^b/', include('posts.urls')),

    # Accounts
    url(r'accounts/', include('social_auth.urls')),
    url(r'accounts/logout/$', 'views.logout_page', name='logout_page'),

    # Warmup
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),

    # Django Admin
    (r'^admin/', include(admin.site.urls)),

    # TinyMCE
    (r'^tinymce/', include('tinymce.urls')),

    # Profiles
    url(r'^profile-redirect/$', 'views.profile_redirect', name='profile_redirect'),
    (r'^p/create/', 'profiles.views.create_profile', {'form_class': UserProfileForm,}),
    (r'^p/(?P<username>\w+)/$', 'profiles.views.profile_detail',
        {
            'extra_context': {
                              'object_list':Entry.objects.all(),
                              'company_list':Company.objects.all(),
                              },
        }),
    (r'^p/edit', 'profiles.views.edit_profile',
        {
        'form_class': UserProfileForm,
        'success_url':'/profile-redirect/',
        }),
    (r'^p/', include('profiles.urls'),),

    # Feeds
    (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}, ),

    # SiteMap
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index',
        {'sitemaps': sitemaps}, name='sitemap'),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps},),

)

