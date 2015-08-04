from django.shortcuts import render, Http404

def proxy(request):
    raise Http404("Not found! Proxying is handled by the webserver and *not* Django. You are seeing this error because the webserver is not configured to proxy requests as expected")
