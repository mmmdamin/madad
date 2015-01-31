from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('account.views',
                       url(r'^login/$', 'login', name='home'),
                       url(r'^logout/?$', 'logout', name='logout'),

                       url(r'^dashboard/$', 'dashboard', name='dashboard'),
)