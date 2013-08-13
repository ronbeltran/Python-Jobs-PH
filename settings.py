# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os
import sys

# add apps directory to python path
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))

# Uncomment this if you're using the high-replication datastore.
# TODO: Once App Engine fixes the "s~" prefix mess we can remove this.
DATABASES['default']['HIGH_REPLICATION'] = True

# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
DBINDEXER_SITECONF = 'dbindexes'

SECRET_KEY = 'parcies=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'django.contrib.markup',
    'django.contrib.humanize',
    'djangotoolbox',
    'dbindexer',
    'permission_backend_nonrel',

    # internal apps
    'accounts',
    'jobs',
    'posts',

    # external apps
    'analytics',
    'autoload',
    'social_auth',
    'profiles',
    'tinymce',

    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'dbindexer.middleware.DBIndexerMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.middleware.csrf.CsrfResponseMiddleware',
    'autoload.middleware.AutoloadMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
#    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.csrf',
    'context_processors.context_variables',

)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'


# django-autoload
AUTOLOAD_SITECONF = 'indexes'

ADMIN_MEDIA_PREFIX = '/media/admin/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
MEDIA_URL = '/static/'

ROOT_URLCONF = 'urls'

#https://github.com/omab/django-social-auth
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleBackend',
    'permission_backend_nonrel.backends.NonrelPermissionBackend',
)

LOGIN_URL = '/accounts/login/google/'
LOGIN_ERROR_URL = '/'
LOGIN_REDIRECT_URL = '/profile-redirect/'

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

SOCIAL_AUTH_EXPIRATION = 'expires'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
SOCIAL_AUTH_ENABLED_BACKENDS = ('google',)
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/p/edit'

SITE_NAME = 'Python Jobs PH (Beta)'
SITE_DESCRIPTION = 'free job postings for python developers'
SITE_KEYWORDS = (
    'Pinoy','Python','Users',
    'Jobs','Pythonista',
    'Web','Developers',
)
SITE_AUTHOR = 'Ronnie B. Beltran'

#django-dbindexer
DBINDEXER_BACKENDS = (
    'dbindexer.backends.BaseResolver',
    'dbindexer.backends.InMemoryJOINResolver',
)

URCHIN_ID = 'UA-19098176-9'

# django-pagination
PAGINATION_DEFAULT_PAGINATION = 15
PAGINATION_INVALID_PAGE_RAISES_404 = True
PAGINATION_DEFAULT_WINDOW = 5 

SITE_ID = 1 

# cache backend
#if DEBUG:
#    CACHE_MIDDLEWARE_SECONDS = 0 # dont cache in dev 
#else:
#    CACHE_MIDDLEWARE_SECONDS = 60*15 # cache for 15 mins
#CACHE_BACKEND = 'memcached://?timeout=0'
#CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True # dont cache requests made by logged in user

# TinyMCE
TINYMCE_JS_URL = os.path.join(MEDIA_URL, "js/tiny_mce/tiny_mce.js")
TINYMCE_JS_ROOT = os.path.join(MEDIA_URL, "js/tiny_mce")
JS_ROOT = os.path.join(MEDIA_URL, "js/tiny_mce")
TINYMCE_DEFAULT_CONFIG = {
        'plugins': "autoresize,spellchecker",
        'theme': 'advanced', 
        'relative_urls': False,
        'cleanup_on_startup': True,
        'custom_undo_redo_levels': 10,
    }
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = False

#import logging
#logging.basicConfig(
#    level = logging.DEBUG,
#    format = '%(asctime)s %(levelname)s %(message)s',
#)

