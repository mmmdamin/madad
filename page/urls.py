from django.conf.urls import patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('page.views',
                       url(r'^(?P<year_num>\d+)/(?P<term_num>\d+)$', 'term_year', name='term'),
                       url(r'^(?P<year_num>\d+)/(?P<term_num>\d+)/(?P<course_num>\d+)/(?P<group_num>\d+)$', 'course',
                           name='course'),

)