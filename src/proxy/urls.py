from django.conf.urls import patterns, include, url
from proxy import views

urlpatterns = patterns('',
    url(r'', views.proxy, name='proxy'),
)
