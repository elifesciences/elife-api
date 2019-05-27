from django.conf.urls import url
from proxy import views

urlpatterns = [
    url(r'', views.proxy, name='proxy'),
]
