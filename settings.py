#coding=utf8
# Django settings for dbss project.
import os
from django.conf import global_settings
import dbss.email_settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEFAULT_FROM_EMAIL = dbss.email_settings.DEFAULT_FROM_EMAIL
EMAIL_HOST= dbss.email_settings.EMAIL_HOST
EMAIL_PORT = dbss.email_settings.EMAIL_PORT
EMAIL_HOST_USER = dbss.email_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = dbss.email_settings.EMAIL_HOST_PASSWORD


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'whysos',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '9884108',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = '*'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/myweb/dbss/dbss/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/myweb/dbss/dbss/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'g_zu8$eh1_#gl+#isywn7_0*5__^xc1*bctm1hwu3s9@de$&yj'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
     'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'corsheaders.middleware.CorsMiddleware',
	#'dbss.mymiddleware.myapploginrequired.MyappLoginRequired',
)

ROOT_URLCONF = 'dbss.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dbss.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	'/myweb/dbss/dbss/templates/',
	'/myweb/dbss/dbss/cardspace/templates/',
	'/myweb/dbss/dbss/user_auth/templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
	'captcha',
	'avatar',
    'haystack',
    'ckeditor',
    'rest_framework',
    'registration',
    'django_rq',
    'django_rq_dashboard',
    'corsheaders',
	'dbss.user_auth',
	'dbss.cardspace',
	'dbss.action',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters':{
        'rq_console':{
            'format':'%(asctime)s %(message)s',
            'datefmt':'%H:%M:%S',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'rq_console':{
            'level':'DEBUG',
            'class':'rq.utils.ColorizingStreamHandler',
            'formatter':'rq_console',
            'exclude':['%(asctime)s'],
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'rq.worker':{
            'handlers':['rq_console',],
            'level':'DEBUG',
        }
    }
}

HAYSTACK_CONNECTIONS = {
    'default' : {
        'ENGINE' : 'dbss.whoosh_cn_backend.WhooshEngine',
        'PATH' : os.path.join(os.path.dirname(__file__),'whoosh_index'),
    },
}


AUTH_USER_MODEL='user_auth.MyUser'
REQUIRED_LOGIN_PATH='/login/'
LOGIN_URL = '/account/login/'
TEMPLATE_CONTEXT_PROCESSORS= global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
	'django.core.context_processors.request',
	'django.contrib.auth.context_processors.auth',
)

LOGIN_REQUIRED_APP = []
LOGIN_REQUIRED_NAME = ['friendslist',]
DEFAULT_CHARSET="utf-8"
CKEDITOR_UPLOAD_PATH = 'upload/'
CKEDITOR_CONFIGS = {
    'default': {
        'language': 'zh-cn',
        'width':'inherit',
        'resize':'False',
        'toolbar': [['Bold', 'Italic', 'Underline'], ['Image', 'Flash'], ['Smiley'], ['Undo', 'Redo'],],
    }
}
WHITE_HTML_TAGS={
    'p': {},
    'strong': {},
    'em': {},
    'u': {},
    'b': {},
    'img':{'src': '^(http://|\/media|\/static)(.*)\S{1,}\.(jpg|png|jpeg|gif)$','height': '^\d{1,3}px$', 'width': '^\d{1,3}px$'},
    'object':{'classid': '^clsid:d27cdb6e-ae6d-11cf-96b8-444553540000$','codebase': '^http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,40,0$',},
    'param':{'name':'^(allowFullScreen|movie)$','value':'(^http://(.*)\S{1,}\.swf$)|(^true$)'},
    'embed':{'allowfullscreen':'^true$', 'pluginspage':'^http://www.macromedia.com/go/getflashplayer$', 'type': 'application/x-shockwave-flash', 'src': '^(http://|\/media|\/static)(.*)\S{1,}\.swf$','height': '^\d{1,3}px$', 'width': '^\d{1,3}px$', "allowFullScreen": "true"},
}
ACCOUNT_ACTIVATION_DAYS = 7
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_IMAGE_BACKEND = 'pillow'
CORS_ALLOW_METHOD = (
    'GET'
)
CARD_IMG_MAX = (600,600)
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'unix:/tmp/redis.sock:0',
        'OPTIONS':{
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    },
    'djrq': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'unix:/tmp/redis.sock:1',
        'OPTIONS':{
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'MAX_ENTRIES':5000,
        }
    },
    'remail': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'unix:/tmp/redis.sock:2',
        'OPTIONS':{
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'MAX_ENTRIES':5000,
        }
    },
    'feed_storage': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'unix:/tmp/redis.sock:3',
        'OPTIONS':{
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'MAX_ENTRIES':5000,
        }
    },
    'favlist': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'unix:/tmp/redis.sock:4',
        'OPTIONS':{
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'MAX_ENTRIES':5000,
        }
    },
    'graphic': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'unix:/tmp/redis.sock:5',
        'OPTIONS':{
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'MAX_ENTRIES':5000,
        }
    },
    'message': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'unix:/tmp/redis.sock:6',
        'OPTIONS':{
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'MAX_ENTRIES':5000,
        }
    },
    'msgrq': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'unix:/tmp/redis.sock:7',
        'OPTIONS':{
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'MAX_ENTRIES':5000,
        }
    },
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
AVATAR_UPDATE_SIZES=[(30,30),(50,50),(80,80),(190,190)]

RQ_QUEUES = {
    'default':{
        'USE_REDIS_CACHE':'default',
    },
    'feed':{
        'USE_REDIS_CACHE': 'djrq',
    },
    'remail':{
        'USE_REDIS_CACHE': 'remail',
    },
    'msgrq':{
        'USE_REDIS_CACHE': 'msgrq',
    }
}
RQ_SHOW_ADMIN_LINK = True
USER_PUBLIC_FEED = '_otherview'
