from django.conf.urls import patterns, include, url
from router import views

urlpatterns = patterns('',
    url(r'^v2/hello_world', views.hello_world),
    url(r'^v2/(?P<doi>[!/]*[/]{0,1}.+)/pdf$', views.pdf),
    url(r'^v2/(?P<doi>[!/]*[/]{0,1}.+)/pdf/(?P<type>article|figures)', views.pdf_by_type),
    #url(r'^v1/pdf/(?P<doi>[!/]*[/]{0,1}.+)', views.pdf),
    url(r'^v2/(?P<arg1>[a-zA-Z]{1,3})/(?P<arg2>\d{1,5})/', views.example_route),
)

