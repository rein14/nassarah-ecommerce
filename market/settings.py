
import os
from decimal import Decimal as D
from oscar.defaults import *
import dj_database_url
 
 
# import oscar
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sp$$@%5t*=jg78uo+2__f37!5#zethce&-&bv6-2cs5*#2&0-e'

# SECURITY WARNING: don't run with debug turned on i.n production!
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "192.168.43.156", "nasarah.herokuapp.com"]

'''
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
'''

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Application definition
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    # 'easyrec',

    # 'compressor',
    # 'select2',
    #'apps.oscar_accounts',

    'widget_tweaks',
    'apps.cashondelivery',
    'apps.mobilemoney',
    'apps.bank',
    #'paypal'
    'pwa',
    'debug_toolbar',
    #'apps.oscar_support',
    #'stores'
    'storages'
 
]

#   INTERNAL_IPS = ['127.0.0.1', '192.168.43.156']


from oscar import get_core_apps
INSTALLED_APPS = INSTALLED_APPS + get_core_apps([
   'apps.address',
   'apps.checkout',
   'apps.shipping',
   'apps.dashboard',
   'apps.order',
   'apps.promotions',
   
    ])


OSCAR_PAYMENT_METHODS = (
    ('cod', 'Cash on delivery'),
    ('mobilemoney', 'mobile money'),
    ('bank','Bank payment'),
)

SITE_ID = 1

USE_I18N = True
# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # Allow languages to be selected
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',

    # Ensure a valid basket is added to the request instance for every request
    'oscar.apps.basket.middleware.BasketMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    
    'debug_toolbar.middleware.DebugToolbarMiddleware'

    

]


HAYSTACK_CONNECTIONS = {
    'default': {
       'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}



AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
'''
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        'INCLUDE_SPELLING': True,
    },
}
'''
HAYSTACK_DJANGO_CT_FIELD = 'django_ct'

ROOT_URLCONF = 'market.urls'

from oscar import OSCAR_MAIN_TEMPLATE_DIR

TEMPLATES = [
    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
           #  ACCOUNTS_TEMPLATE_DIR,
        ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'loaders': [
                #'django.template.loaders.cached.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',

            ],
            'context_processors': [
                
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',

                # Oscar specific
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.core.context_processors.metadata',
            ],

            'debug': DEBUG,


        }
    }
]


WSGI_APPLICATION = 'market.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    }
}
'''
DATABASES = {'default': dj_database_url.config(default='postgres://stnpdqluadmshq:131dedce59cf2e69b34f45540ae02fd275074e2d9201130bd2da4fd284c8d2d4@ec2-54-221-225-11.compute-1.amazonaws.com:5432/df7i6d16k12oeh')}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/



def location(x): return os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

AWS_ACCESS_KEY_ID = 'AKIAIXJ6TVKSOC6ABAPA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'nasara'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIA_URL = '/media/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'market.storage_backends.MediaStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# ==============
# apps settings
# ==============

from collections import OrderedDict

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
OSCAR_SETTINGS = dict(
    [(k, v) for k, v in locals().items() if k.startswith('OSCAR_')])

OSCAR_SHOP_NAME = 'Ambez'
OSCAR_SHOP_TAGLINE = 'Number One Stop Shop'
OSCAR_HOMEPAGE = reverse_lazy('promotions:home')

# Basket settings
OSCAR_BASKET_COOKIE_LIFETIME = 7 * 24 * 60 * 60
OSCAR_BASKET_COOKIE_OPEN = 'oscar_open_basket'
OSCAR_BASKET_COOKIE_SECURE = False
OSCAR_MAX_BASKET_QUANTITY_THRESHOLD = 10000

# Recently-viewed products
OSCAR_RECENTLY_VIEWED_COOKIE_LIFETIME = 7 * 24 * 60 * 60
OSCAR_RECENTLY_VIEWED_COOKIE_NAME = 'oscar_history'
OSCAR_RECENTLY_VIEWED_COOKIE_SECURE = False
OSCAR_RECENTLY_VIEWED_PRODUCTS = 20

# Currency
OSCAR_DEFAULT_CURRENCY = 'GHC '

# Paths
OSCAR_IMAGE_FOLDER = 'images/products/%Y/%m/'
OSCAR_PROMOTION_FOLDER = 'images/promotions/'
OSCAR_DELETE_IMAGE_FILES = True

# Copy this image from oscar/static/img to your MEDIA_ROOT folder.
# It needs to be there so Sorl can resize it.
OSCAR_MISSING_IMAGE_URL = 'image_not_found.jpg'
OSCAR_UPLOAD_ROOT = '/tmp'

# Address settings
OSCAR_REQUIRED_ADDRESS_FIELDS = ('first_name', 'last_name','line4', 'line1',
    'phone_number', 'country')

# Pagination settings

OSCAR_OFFERS_PER_PAGE = 30
OSCAR_PRODUCTS_PER_PAGE = 30
OSCAR_REVIEWS_PER_PAGE = 20
OSCAR_NOTIFICATIONS_PER_PAGE = 20
OSCAR_EMAILS_PER_PAGE = 20
OSCAR_ORDERS_PER_PAGE = 20
OSCAR_ADDRESSES_PER_PAGE = 20
OSCAR_STOCK_ALERTS_PER_PAGE = 20
OSCAR_DASHBOARD_ITEMS_PER_PAGE = 20

OSCAR_SHOP_TAGLINE = '  AMbez'
OSCAR_RECENTLY_VIEWED_PRODUCTS = 10
# Checkout
OSCAR_ALLOW_ANON_CHECKOUT = True

# Promotions
COUNTDOWN, LIST, SINGLE_PRODUCT, TABBED_BLOCK = (
    'Countdown', 'List', 'SingleProduct', 'TabbedBlock')
OSCAR_PROMOTION_MERCHANDISING_BLOCK_TYPES = (
    (COUNTDOWN, "Vertical list"),
    (LIST, "Horizontal list"),
    (TABBED_BLOCK, "Tabbed block"),
    (SINGLE_PRODUCT, "Single product"),
)
OSCAR_PROMOTION_POSITIONS = (('page', 'Page'),
                             ('right', 'Right-hand sidebar'),
                             ('coupons', 'Coupons'),
                             ('categories', 'Categories'),
                             ('another', 'Another'),
                             ('undercats', 'Undercats'),
                             ('arrivals', 'Arrivals'),
                             ('offers', 'Offers'),
                             ('banner', 'Banner '),
                             ('left', 'Left-hand sidebar'),
                             ('picture', 'pictures'),
                             ('featured','featured_brand'))

# Reviews
OSCAR_ALLOW_ANON_REVIEWS = True
OSCAR_MODERATE_REVIEWS = False

# Accounts
OSCAR_ACCOUNTS_REDIRECT_URL = 'customer:profile-view'

# This enables sending alert notifications/emails instantly when products get
# back in stock by listening to stock record update signals.
# This might impact performance for large numbers of stock record updates.
# Alternatively, the management command ``oscar_send_alerts`` can be used to
# run periodically, e.g. as a cron job. In this case eager alerts should be
# disabled.
OSCAR_EAGER_ALERTS = True

# Registration
OSCAR_SEND_REGISTRATION_EMAIL = True
OSCAR_FROM_EMAIL = 'no@name.com'

# Slug handling
OSCAR_SLUG_FUNCTION = 'oscar.core.utils.default_slugifier'
OSCAR_SLUG_MAP = {}
OSCAR_SLUG_BLACKLIST = []
OSCAR_SLUG_ALLOW_UNICODE = False

# Cookies
OSCAR_COOKIES_DELETE_ON_LOGOUT = ['oscar_recently_viewed_products', ]

# Hidden Oscar features, e.g. wishlists or reviews
OSCAR_HIDDEN_FEATURES = []

# Menu structure of the dashboard navigation
OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': _('Dashboard'),
        'icon': 'icon-th-list',
        'url_name': 'dashboard:index',
    },
    {
        'label': _('Behaviour'),
        'icon': 'icon-list', 
        'url_name': 'dashboard:analytics',
    },  
  {
                'label': _('Products'),
                'icon': 'icon-sitemap',
                'url_name': 'dashboard:catalogue-product-list',
            },
    {
        'label': _('Catalogue Options'),
        'icon': 'icon-sitemap',
        'children': [
           
            {
                'label': _('Product Types'),
                'url_name': 'dashboard:catalogue-class-list',
            },
            {
                'label': _('Categories'),
                'url_name': 'dashboard:catalogue-category-list',
            },
            {
                'label': _('Ranges'),
                'url_name': 'dashboard:range-list',
            },
            {
                'label': _('Low stock alerts'),
                'url_name': 'dashboard:stock-alert-list',
            },
        ]
    },
  
     {
        'label': _('Fulfilment'),
        'icon': 'icon-shopping-cart',
        'children': [
            {
                'label': _('Orders'),
                'url_name': 'dashboard:order-list',
            },
            {
                'label': _('Statistics'),
                'url_name': 'dashboard:order-stats',
            },
            {
                'label': _('Partners'),
                'url_name': 'dashboard:partner-list',
            },
            # The shipping method dashboard is disabled by default as it might
            # be confusing. Weight-based shipping methods aren't hooked into
            # the shipping repository by default (as it would make
            # customising the repository slightly more difficult).
            # {
            #   'label': _('Shipping charges'),
            #   'url_name': 'dashboard:shipping-method-list',
            # },
        ]},
    {
        'label': _('Payments'),
        'icon': 'icon-money',
        'children': [
            {
                'label': _('COD transactions'),
                'url_name': 'cashondelivery-transaction-list',
            },
            {
                'label': _('MOMO transactions'),
                'url_name': 'mobilemoney-transaction-list',
            },
            {
                'label': _('BANK transactions'),
                'url_name': 'bank-transaction-list',
            },
        ]
    },
    {
        'label': _('Customers'),
        'icon': 'icon-group',
        'children': [
            {
                'label': _('Customers'),
                'url_name': 'dashboard:users-index',
            },
            {
                'label': _('Stock alert requests'),
                'url_name': 'dashboard:user-alert-list',
            },
        ]
    },
    {
        'label': _('Offers'),
        'icon': 'icon-bullhorn',
        'children': [
            {
                'label': _('Offers'),
                'url_name': 'dashboard:offer-list',
            },
            {
                'label': _('Vouchers'),
                'url_name': 'dashboard:voucher-list',
            },
            {
                'label': _('Voucher Sets'),
                'url_name': 'dashboard:voucher-set-list',
            },
        ],
    },
    {
        'label': _('Content'),
        'icon': 'icon-folder-close',
        'children': [
            {
                'label': _('Content blocks'),
                'url_name': 'dashboard:promotion-list',
            },
            {
                'label': _('Content blocks by page'),
                'url_name': 'dashboard:promotion-list-by-page',
            },
            {
                'label': _('Pages'),
                'url_name': 'dashboard:page-list',
            },
            {
                'label': _('Email templates'),
                'url_name': 'dashboard:comms-list',
            },
            {
                'label': _('Reviews'),
                'url_name': 'dashboard:reviews-list',
            },
        ]
    },
    {
        'label': _('Reports'),
        'icon': 'icon-bar-chart',
        'url_name': 'dashboard:reports-index',
    },

    {
        'label': 'Accounts',
        'icon': 'icon-globe',
        'children': [
            {
                'label': 'Accounts',
                'url_name': 'accounts-list',
            },
            {
                'label': 'Transfers',
                'url_name': 'transfers-list',
            },
            {
                'label': 'Deferred income report',
                'url_name': 'report-deferred-income',
            },
            {
                'label': 'Profit/loss report',
                'url_name': 'report-profit-loss',
            },
        ]
    },
    {
        'label': 'Accounts',
        'icon': 'icon-globe',
        'children': [
            {
                'label': 'Accounts',
                'url_name': 'accounts-list',
            },
            {
                'label': 'Transfers',
                'url_name': 'transfers-list',
            },
            {
                'label': 'Deferred income report',
                'url_name': 'report-deferred-income',
            },
            {
                'label': 'Profit/loss report',
                'url_name': 'report-profit-loss',
            },
        ]
    },
     
   
]


OSCAR_DASHBOARD_DEFAULT_ACCESS_FUNCTION = 'oscar.apps.dashboard.nav.default_access_fn'  # noqa

# Search facets
OSCAR_SEARCH_FACETS = {
    'fields': OrderedDict([
        # The key for these dicts will be used when passing facet data
        # to the template. Same for the 'queries' dict below.
        #('product_class', {'name': _('Type'), 'field': 'product_class'}),
        ('rating', {'name': _('Rating'), 'field': 'rating'}),
        # You can specify an 'options' element that will be passed to the
        # SearchQuerySet.facet() call.
        # For instance, with Elasticsearch backend, 'options': {'order': 'term'}
        # will sort items in a facet by title instead of number of items.
        # It's hard to get 'missing' to work
        # correctly though as of Solr's hilarious syntax for selecting
        # items without a specific facet:
        # http://wiki.apache.org/solr/SimpleFacetParameters#facet.method
        # 'options': {'missing': 'true'}
    ]),
    'queries': OrderedDict([
        ('price_range',
         {
             'name': _('Price range'),
             'field': 'price',
             'queries': [
                 # This is a list of (name, query) tuples where the name will
                 # be displayed on the front-end.
                 (_('0 to 20'), u'[0 TO 20]'),
                 (_('20 to 40'), u'[20 TO 40]'),
                 (_('40 to 60'), u'[40 TO 60]'),
                 (_('60+'), u'[60 TO *]'),
             ]
         }),
    ]),
}

OSCAR_PROMOTIONS_ENABLED = True
OSCAR_PRODUCT_SEARCH_HANDLER = None

# Meta
# ====



# Order processing
# ================

# Sample order/line status settings. This is quite simplistic. It's like you'll
# want to override the set_status method on the order object to do more
# sophisticated things.
OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'

# This dict defines the new order statuses than an order can move to
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Complete', 'Cancelled',),
    'Cancelled': (),
    'Complete': (),
}
# This dict defines the line statuses that will be set when an order's status
# is changed   
OSCAR_LINE_STATUS_PIPELINE = OSCAR_ORDER_STATUS_PIPELINE

OSCAR_ORDER_STATUS_CASCADE = {
     'Being processed': 'Being processed',
    'Cancelled': 'Cancelled',
    'Complete': 'Shipped',
}
# LESS/CSS
# ========

# We default to using CSS files, rather than the LESS files that generate them.
# If you want to develop Oscar's CSS, then set OSCAR_USE_LESS=True to enable the
# on-the-fly less processor.
OSCAR_USE_LESS = False

PWA_APP_NAME = 'Nasarah'
PWA_APP_DESCRIPTION = "Do kickass things all day long without that pesky browser chrome"
PWA_APP_THEME_COLOR = '#1861a5'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
        'src': '/static/oscar/img/logo/logo.png',
        'sizes': '160x160'
    }
]
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/oscar/js/serviceworker.js')

import dj_database_url
import os

DATABASES = {
      'default': dj_database_url.config(
          default='sqlite:////{0}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
      )
  }
  
#SESSION_SERIALIZER ='django.contrib.sessions.serializers.PickleSerializer'
#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

