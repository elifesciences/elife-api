#from django.db import models

# Create your models here.

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
            
class media_file():
    def __init__ (self, doi, xlink, filetype):
        self.doi = doi
        self.xlink = xlink
        self.filetype = filetype
        
    def get_doi_id(self):
        """
        Parse DOI value which can be number or string
        """
        try:
            return int(self.doi)
        except ValueError:
            return int(self.doi.split('.')[-1])
        
    def get_baseurl(self):
        if self.filetype == "jpg":
            return ('http://cdn.elifesciences.org/elife-articles/'
                            + str(self.get_doi_id()).zfill(5)
                            + '/jpg'
                            + '/')
    
    def get_url(self):
        if self.filetype == "jpg":
            return (self.get_baseurl()
                    + self.xlink
                    + '.jpg')
