from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('base.views',
                       url(r'^$', 'home', name='home'),

)