from django.conf.urls import include, url
from django.contrib import admin
from oscar.app import application
from django.conf import settings
from django.conf.urls.static import static
from apps.cashondelivery.dashboard.app import application as cod_app

from apps.mobilemoney.dashboard.app import application as momo_app
from apps.bank.dashboard.app import application as bank_app

from .views import CouponView
from oscar.apps.search.views import autocomplete        
#from apps.oscar_accounts.dashboard.app import application as accounts_app
#from apps.oscar_accounts.views import AccountBalanceView
#from paypal.express.dashboard.app import application

#from oscar_support.app import application as support
#from oscar_support.api.app import application as support_api
#from oscar_support.dashboard.app import application as support_dashboard


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # The Django admin is not officially supported; expect breakage. # Nonetheless, it's often useful for debugging.\
    # url(r'^admin/', include(admin.site.urls)),
    url(r'', include(application.urls)),
    #url(r'^giftcard-balance/', AccountBalanceView.as_view(),name="account-balance"),
    url(r'^dashboard/cod/', include(cod_app.urls)),
    url(r'^dashboard/momo/', include(momo_app.urls)),
     url(r'^dashboard/bank/', include(bank_app.urls)),

    url(r'^coupon/$', CouponView.as_view(), name='coupon'),
    url(r'^autocomplete/', autocomplete, name='autocomplete'),
    url(r'', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    #url(r'^dashboard/accounts/', include(accounts_app.urls)),
    #url(r'^dashboard/paypal/express/', include(application.urls)),
    #url(r'^dashboard/support/', include(support_dashboard.urls)),
    #url(r'', include(support.urls)),
    #url(r'^api/', include(support_api.urls)), # You can use instead Oscar api urls

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
