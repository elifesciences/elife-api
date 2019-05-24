from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET
import requests
import json
from models import PdfFile, MediaFile
from annoying.decorators import render_to
from os.path import join
from django.conf import settings

@render_to('router/index.html')
def index(request):
    return {
        'readme': open(join(settings.PROJECT_DIR, 'README.md'), 'r').read()
    }

def check_url_exists(url):
    """
    Check if a URL exists by HEAD request
    """
    if url is None:
        return None
    
    r = requests.head(url, allow_redirects=True)
    if r.status_code == requests.codes.ok:
        return r.url
    else:
        return None
    return None

def json_response(data, status=200):
    return HttpResponse(json.dumps(data, indent=4), content_type="application/json", status=status)

@require_GET
def hello_world(request):
    return json_response({"message": "Hello, world!"})

@require_GET
def example_route(request, arg1, arg2):
    """
    This text description for this API call
    arg1 -- A first argument
    arg2 -- A second argument
    """
    return HttpResponseRedirect('http://example.org/%s/%s/' % (arg1, arg2))

@require_GET
def pdf(request, doi, type = None):
    """
    Get PDF file locations in JSON format.
    """
    
    pdf_types = ['figures','article']
    
    if type:
        types = []
        types.append(type)
    else:
        types = pdf_types

    data = []
    notes = []
    for pdf_type in types:
        try:
            pdf = PdfFile(doi, pdf_type)
            
            # Check if URL exists
            if check_url_exists(pdf.get_url()) is not None:
                # Add data from the object
                item = {}
                item['doi'] = pdf.get_doi()
                item['doi_id'] = pdf.get_doi_id()
                item['file_type'] = pdf.file_type
                item['url'] = pdf.get_url()
                item['size'] = pdf.get_size_from_s3()
                item['type'] = pdf.type
                data.append(item)
            else:
                # Append notes
                #notes.append('%s does not exist' % pdf.get_url())
                pass
               
        except:
            return HttpResponse(status=404) #status.HTTP_404_NOT_FOUND)

    response_list = {}
    response_list['data'] = data
        
    # Add metadata
    if len(notes) > 0:
        response_list['notes'] = notes
    response_list['results'] = len(data)

    return json_response(response_list)

@require_GET
def pdf_by_type(request, doi, type):
    """
    Get a PDF file URI
    The pdf_type can be 'figures' or 'article'
    """
    return pdf(request, doi, type)
    
@require_GET
def media(request, doi, xlink = None, type = None, redirect = None):
    """
    Get media file locations in JSON format.
    """
    
    data = []
    file = None
    
    # Given a DOI, xlink and type
    if doi is not None and xlink is not None and type is not None:
        file = MediaFile(doi, xlink, type)
        if check_url_exists(file.get_url()) is not None:
            # Add data
            item = {}
            item['type'] = file.type
            item['doi'] = file.get_doi()
            item['doi_id'] = file.get_doi_id()
            item['url'] = file.get_url()
            data.append(item)
    
    response_list = {}
    response_list['data'] = data
    response_list['results'] = len(data)

    query_params = request.GET
    
    if (
        (redirect is True or query_params.get('redirect') is not None)
        and len(response_list['data']) == 1):
        
        return HttpResponseRedirect(response_list['data'][0]['url'])
    
    elif ((redirect is True or query_params.get('redirect') is not None)
        and len(response_list['data']) < 1):
    
        # No URL return and redirect, error 404
        return HttpResponse(status=404)
    
    else:
        # Default with no redirect, return all the data
        return json_response(response_list)
    
@require_GET
def media_file(request, doi, filename):
    """
    Get a specific media file
    and redirect to the file after locating the file at the third-party media provider
    Specifically this is useful in displaying videos in eLife Lens
    
    filename includes the name and file extension, e.g. 'elife00007v001.jpg' or 'elife00007v001.mp4'
    """
    
    try:
        xlink = filename.split(".")[0]
        type = filename.split(".")[1]
    except:
        xlink = None
        type = None

    redirect = True
    
    return media(request, doi, xlink, type, redirect)
    
@require_GET
def media_xlink_format(request, doi, xlink, type):
    """
    Get a specific media file by specifying the xlink and type
    type for videos can be 'jpg', 'mp4', 'ogv', 'webm'
    
    redirect -- If set (to any value) redirect to the URL
    """
    return media(request, doi, xlink, type)

