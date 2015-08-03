from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'', include('router.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    # Examples:
    # url(r'^$', 'core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)
