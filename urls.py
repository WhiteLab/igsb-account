from django.conf.urls import url
from django.views.generic import TemplateView

import views

urlpatterns = [
    url(r'^$', views.home, name='create_home'),
    url(r'^create/$', views.create, name='create_account'),
    url(r'^create/success/(?P<account_name>\w+)/$', views.create_success, name='create_success'),
    url(r'^create/already-exists/(?P<account_name>\w+)/$', views.create_already_exists,
        name='create_already_exists'),
    url(r'^create/error/$', TemplateView.as_view(template_name='account/error.html'),
        name='create_error')
]