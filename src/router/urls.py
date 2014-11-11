from django.conf.urls import patterns, include, url
from router import views

urlpatterns = patterns('',
    url(r'^v1/hello_world', views.hello_world),
    url(r'^v1/pdf', views.pdf), 
    url(r'v1/(?P<arg1>[a-zA-Z]{1,3})/(?P<arg2>\d{1,5})/', views.example_route),
)

