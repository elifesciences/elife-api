#from django.db import models
import requests

# Create your models here.

class eLifeFile():
    """
    Base class for a file in the eLife system,
    a place for common code
    """
    def __init__ (self):
        self.cdn_base_url = 'http://cdn.elifesciences.org/'
        self.figure_pdf_base_url = 'http://s3.amazonaws.com/elife-figure-pdfs/'
        self.cdn_articles_folder = 'elife-articles/'
        self.glencoe_api_base_url = 'http://movie-usa.glencoesoftware.com/'
        self.glencoe_metadata_endpoint = 'metadata/'
    
    def get_doi_id(self):
        """
        Parse DOI value which can be number or string
        """
        try:
            return int(self.doi)
        except ValueError:
            return int(self.doi.split('.')[-1])
            
    def get_doi(self):
        """
        Return the full DOI
        """
        return '10.7554/eLife.' + str(self.get_doi_id()).zfill(5)

class PdfFile(eLifeFile):
    def __init__ (self, doi, type):
        eLifeFile.__init__(self)
        self.doi = doi
        self.type = type
        
    def get_baseurl(self):
        if self.type == "figures":
            return self.figure_pdf_base_url
        elif self.type == "article":
            return (self.cdn_base_url + self.cdn_articles_folder
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
            
class MediaFile(eLifeFile):
    def __init__ (self, doi, xlink, filetype):
        eLifeFile.__init__(self)
        self.doi = doi
        self.xlink = xlink
        self.filetype = filetype
        
    def get_baseurl(self):
        if self.filetype == "jpg":
            return (self.cdn_base_url + self.cdn_articles_folder
                            + str(self.get_doi_id()).zfill(5)
                            + '/jpg'
                            + '/')
    
    def get_url(self):
        if self.filetype == "jpg":
            return (self.get_baseurl()
                    + self.xlink
                    + '.jpg')
        elif self.filetype in ['mp4', 'webm', 'ogv']:
            return self.get_url_from_glencoe(self.filetype)

    def get_url_from_glencoe(self, filetype):
        url = self.glencoe_api_base_url + self.glencoe_metadata_endpoint + self.get_doi()
        r = requests.get(url, allow_redirects=True)
        
        video_json = None
        if r.status_code == requests.codes.ok:
            for video in r.json:
                # Get one of the URLs to compare with the xlink
                try:
                    video_xlink =  r.json[video]['ogv_href'].split('/')[-1].split('.')[0]
                except:
                    video_xlink = None
                if video_xlink == self.xlink:
                    video_json = r.json[video]
                    
        if video_json:
            if self.filetype == "mp4":
                return video_json['mp4_href']
            elif self.filetype == "webm":
                return video_json['webm_href']
            elif self.filetype == "ogv":
                return video_json['ogv_href']