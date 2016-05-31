from django.conf.urls import url
from django.views.generic import TemplateView

import views

urlpatterns = [
    url(r'^$', views.create_home, name='create_home'),

    url(r'^new/$', views.create_home, name='create_home'),
    url(r'^new/create/$', views.create, name='create_account'),
    url(r'^new/success/(?P<account_name>\w+)/$', views.create_success, name='create_success'),

    url(r'^change/$', views.change_password_home, name='change_home'),
    url(r'^change/password/$', views.change_password, name='change_password'),
    url(r'^change/success/(?P<account_name>\w+)/$', views.change_success, name='change_success'),

    url(r'^error/$', views.error, name='account_error')
]
