from django.shortcuts import render
from django.http import HttpResponseRedirect

def redirect(dest):
    return HttpResponseRedirect(dest)

def example_route(request, arg1, arg2):
    return redirect('http://example.org/%s/%s/' % (arg1, arg2))
