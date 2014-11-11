from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})

def redirect(dest):
    return HttpResponseRedirect(dest)

def example_route(request, arg1, arg2):
    return redirect('http://example.org/%s/%s/' % (arg1, arg2))
