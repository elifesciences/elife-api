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
        self.cdn_articles_folder = 'elife-articles/'
        self.glencoe_api_base_url = 'http://movie-usa.glencoesoftware.com/'
        self.glencoe_metadata_endpoint = 'metadata/'
        
        # Bucket names
        self.cdn_bucket_name = 'elife-cdn'
    
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

            s3_data = self.parse_s3_xml(r.text)
            if s3_data:
                try:
                    return s3_data[prefix]['size']
                except:
                    return None
        else:
            return None

    def parse_s3_xml(self, xml_string):
        """
        Given an XML string from an S3 object query,
        return JSON data about the object named s3_key_name
        Currently supports extracting the Size value at time of writing
        """
        
        s3_data = {}
        
        root = ElementTree.fromstring(xml_string)
        
        for contents_tag in root.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Contents'):
            #print contents_tag.tag
            for key_tag in contents_tag.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Key'):
                #print key_tag.text
                for size_tag in contents_tag.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Size'):
                    if key_tag.text not in s3_data.keys():
                        # Create dict index for the key if not exists already
                        s3_data[key_tag.text] = {}
                    s3_data[key_tag.text]['size'] = int(size_tag.text)
        
        return s3_data

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
            return (self.cdn_articles_folder
                            + str(self.get_doi_id()).zfill(5)
                            + '/' + 'figures-pdf/')
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
            bucket_url = self.s3_base_url + self.cdn_bucket_name
        elif self.type == "article":
            bucket_url = self.s3_base_url + self.cdn_bucket_name
        
        # Can use the filename as part of the prefix
        prefix = self.get_foldername() + self.get_filename()
        
        return eLifeFile.get_size_from_s3(self, bucket_url, prefix)
            
class MediaFile(eLifeFile):
    def __init__ (self, doi, xlink, type):
        eLifeFile.__init__(self)
        self.doi = doi
        self.xlink = xlink
        self.type = type
        
    def get_url(self):
        if self.type in ['mp4', 'webm', 'ogv', 'jpg']:
            return self.get_url_from_glencoe(self.type)

    def get_url_from_glencoe(self, type):
        url = self.glencoe_api_base_url + self.glencoe_metadata_endpoint + self.get_doi()
        r = requests.get(url, allow_redirects=True)
        
        video_json = None
        if r.status_code == requests.codes.ok:
            request_json = r.json()
            for video in request_json:
                # Get one of the URLs to compare with the xlink
                try:
                    video_xlink =  request_json[video]['ogv_href'].split('/')[-1].split('.')[0]
                except:
                    video_xlink = None
                if video_xlink == self.xlink.split('.')[0]:
                    video_json = request_json[video]
                    
        if video_json:
            if self.type == "mp4":
                return video_json['mp4_href']
            elif self.type == "webm":
                return video_json['webm_href']
            elif self.type == "ogv":
                return video_json['ogv_href']
            elif self.type == "jpg":
                return video_json['jpg_href']
