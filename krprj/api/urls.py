from django.conf.urls import patterns

import views

urlpatterns = patterns('',
    (r'^v1/$', views.api_status),
)
