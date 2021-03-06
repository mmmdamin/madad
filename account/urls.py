from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('account.views',
                       url(r'^login/$', 'login', name='login'),
                       url(r'^logout/?$', 'logout', name='logout'),
                       url(r'^change-password/?$', 'password_reset_change', name='password_reset_change'),
                       url(r'^dashboard/$', 'dashboard', name='dashboard'),

                       url(r'^', include('password_reset.urls')),

)