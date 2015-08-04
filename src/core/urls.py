from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^proxy/', include('proxy.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'', include('router.urls')),
)
