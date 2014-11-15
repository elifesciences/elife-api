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
    def __init__ (self, doi, type):
        self.doi = doi
        self.type = type
        
    def get_doi_id(self):
        """
        Parse DOI value which can be number or string
        """
        try:
            return int(self.doi)
        except ValueError:
            return int(self.doi.split('.')[-1])
        
    def get_baseurl(self):
        if self.type == "figures":
            return 'http://s3.amazonaws.com/elife-figure-pdfs/'
        elif self.type == "article":
            return ('http://cdn.elifesciences.org/elife-articles/'
                            + str(self.get_doi_id()).zfill(5)
                            + '/')
            
    def get_url(self):
        
        if self.type == "figures":
            return (self.get_baseurl()
                    + 'elife'
                    + str(self.get_doi_id()).zfill(5)
                    + '-figures.pdf')
        elif self.type == "article":
            return (self.get_baseurl()
                    + 'pdf/'
                    + 'elife'
                    + str(self.get_doi_id()).zfill(5)
                    + '.pdf')

@api_view(['GET'])
def pdf(request, doi):
    """
    Get a PDF file URI
    type -- The type of PDF, 'figures' or 'article'
    """
    
    pdf_types = ['figures','article']
    
    try:
        if request.QUERY_PARAMS['type']:
            # Validate type - TODO!!
            types = []
            types.append(request.QUERY_PARAMS['type'])
    except:
        types = pdf_types
        
    data = []
    for pdf_type in types:
        try:
            pdf = pdf_file(doi, pdf_type)
            
            # Add data
            item = {}
            item['url'] = pdf.get_url()
            item['type'] = pdf_type
            data.append(item)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    response_list = {}
    response_list['data'] = data
        
    # Add metadata
    response_list['results'] = len(data)

    return Response(response_list)

