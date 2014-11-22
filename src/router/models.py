#from django.db import models

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
    
    def get_doi_id(self):
        """
        Parse DOI value which can be number or string
        """
        try:
            return int(self.doi)
        except ValueError:
            return int(self.doi.split('.')[-1])

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
