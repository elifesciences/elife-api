from django.db import models
import requests
from xml.etree import ElementTree

# Create your models here.

class eLifeFile():
    """
    Base class for a file in the eLife system,
    a place for common code
    """
    def __init__ (self):
        self.cdn_base_url = 'http://cdn.elifesciences.org/'
        self.s3_base_url = 'http://s3.amazonaws.com/'
        self.figure_pdf_folder = 'figure-pdf/'
        self.cdn_articles_folder = 'elife-articles/'
        self.glencoe_api_base_url = 'http://movie-usa.glencoesoftware.com/'
        self.glencoe_metadata_endpoint = 'metadata/'
        
        # Bucket names
        self.cdn_bucket_name = 'elife-cdn'
        self.figure_pdf_bucket_name = 'elife-figure-pdfs'
    
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
        
    def get_size_from_s3(self, bucket_url, prefix):
        """
        Get S3 bucket meta for the prefix
        and if the object named prefix exists,
        return the Size in bytes
        """
        
        url = bucket_url + '?prefix=' + prefix
        r = requests.get(url)
        #print url
        if r.status_code == requests.codes.ok:

            root = ElementTree.fromstring(r.text)

            for contents_tag in root.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Contents'):
                #print contents_tag.tag
                for key_tag in contents_tag.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Key'):
                    #print key_tag.text
                    if key_tag.text == prefix:
                        # A match, return the Size
                        for size_tag in contents_tag.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Size'):
                            return int(size_tag.text)

        else:
            return None


class PdfFile(eLifeFile):
    def __init__ (self, doi, type):
        eLifeFile.__init__(self)
        self.doi = doi
        self.type = type
        self.file_type = 'pdf'
        
    def get_foldername(self):
        """
        The folder name depends on the type of PDF
        It is used in both the CDN URL and the S3 bucket URL
        """
        if self.type == "figures":
            return self.figure_pdf_folder
        elif self.type == "article":
            return (self.cdn_articles_folder
                            + str(self.get_doi_id()).zfill(5)
                            + '/' + 'pdf/')
            
    def get_filename(self):
        """
        The filename of the PDF file itself,
        based on the type of PDF and the article DOI
        """
        if self.type == "figures":
            return ('elife'
                    + str(self.get_doi_id()).zfill(5)
                    + '-figures.pdf')
        elif self.type == "article":
            return ('elife'
                    + str(self.get_doi_id()).zfill(5)
                    + '.pdf')
            
    def get_url(self):
        """
        The URL to the file on the Cloudfront CDN
        """
        return self.cdn_base_url + self.get_foldername() + self.get_filename()
            
    def get_size_from_s3(self):
        """
        Get the file size in bytes by using the base object
        """

        # Specify in which bucket the file is stored
        if self.type == "figures":
            bucket_url = self.s3_base_url + self.figure_pdf_bucket_name
        elif self.type == "article":
            bucket_url = self.s3_base_url + self.cdn_bucket_name
        
        # Can use the filename as part of the prefix
        prefix = self.get_foldername() + self.get_filename()
        
        return eLifeFile.get_size_from_s3(self, bucket_url, prefix)
        