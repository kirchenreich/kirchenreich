from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from krprj.worshipmap.urls import urlpatterns as worshipmap_patterns

urlpatterns = patterns('',
    url(r'^api/', include('krprj.api.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += worshipmap_patterns
