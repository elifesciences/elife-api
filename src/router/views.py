from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})

def redirect(dest):
    return HttpResponseRedirect(dest)

@api_view(['GET'])
def example_route(request, arg1, arg2):
    """
    This text description for this API call
    arg1 -- A first argument
    arg2 -- A second argument
    """
        
    # Quick hack to get a Location redirect
    redirect_response = redirect('http://example.org/%s/%s/' % (arg1, arg2))
    headers = {}
    headers['Location'] = redirect_response.url
    return Response(
        status=status.HTTP_302_FOUND,
        headers=headers)

class pdf_file():
    def __init__ (self, doi = None):
        self.doi = doi

    def get_url(self):
        
        doi_id = int(self.doi.split('.')[-1])
        
        return ('http://example.org/'
                + str(doi_id).zfill(5)
                + '/elife'
                + str(doi_id).zfill(5)
                + '.pdf')

@api_view(['GET'])
def pdf(request):
    """
    Get a PDF file URI
    doi -- An article DOI
    """
    
    try:
        pdf = pdf_file(request.QUERY_PARAMS['doi'])
        
        response_list = {}
        response_list['url'] = pdf.get_url()
    
        return Response(response_list)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

