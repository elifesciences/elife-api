from django.conf.urls import include, url

urlpatterns = [
    url(r'^proxy/', include('proxy.urls')),
    url(r'', include('router.urls')),
]
