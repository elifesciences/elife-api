from django.conf.urls import include, url
from proxy import views

urlpatterns = [
    url(r'', views.proxy, name='proxy'),
]
