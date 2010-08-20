from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        view='udoxmailinglist.views.signup',
        name='signup_form'),
    url(r'^mobile/$',
        view='udoxmailinglist.views.mobile_signup',
        name='mobile_signup_form'),
)

