from django.conf.urls import include, url
from router import views

urlpatterns = [
    url(r'^v2/hello_world', views.hello_world),
    url(r'^v2/articles/(?P<doi>[!/]*[/]{0,1}.+)/pdf$', views.pdf),
    url(r'^v2/articles/(?P<doi>[!/]*[/]{0,1}.+)/pdf/(?P<type>article$|figures$)', views.pdf_by_type),
    url(r'^v2/articles/(?P<doi>[!/]*[/]{0,1}.+)/media/file/(?P<filename>\w.+)', views.media_file),
    url(r'^v2/articles/(?P<doi>[!/]*[/]{0,1}.+)/media/(?P<xlink>[!^file]\w.+)/(?P<type>jpg$|mp4$|ogv$|webm$)', views.media_xlink_format),
    #url(r'^v1/pdf/(?P<doi>[!/]*[/]{0,1}.+)', views.pdf),
    url(r'^v2/(?P<arg1>[a-zA-Z]{1,3})/(?P<arg2>\d{1,5})/', views.example_route),

    url(r'^$', views.index),

]

