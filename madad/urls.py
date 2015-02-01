from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'$^', 'page.views.all_term_year', name='home'),
                       url(r'^ckeditor/', include('ckeditor.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include("base.urls")),
                       url(r'^pages/', include("page.urls")),

                       url(r'^accounts/', include("account.urls")),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
