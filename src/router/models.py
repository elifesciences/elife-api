from django.db import models
import requests
import json
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
        # Default: get the URL by type
        if self.type in ['mp4', 'webm', 'ogv', 'jpg']:
            return self.get_url_from_glencoe(self.type)

    def get_url_from_glencoe(self, type, glencoe_json = None):
        if glencoe_json is None:
            glencoe_json = self.glencoe_json()
        
        video_json = self.glencoe_json_by_xlink(glencoe_json)
        
        # Now can filter data by type to get the url
        if video_json:
            for key, val in video_json.iteritems():
                if self.type == "mp4":
                    return val['mp4_href']
                elif self.type == "webm":
                    return val['webm_href']
                elif self.type == "ogv":
                    return val['ogv_href']
                elif self.type == "jpg":
                    return val['jpg_href']

    def glencoe_json_by_xlink(self, glencoe_json):
        """
        Given Glencoe API metadata for a particular article,
        return only the item that matches the xlink for this file object
        """
        if glencoe_json is None:
            return None
        
        if type(glencoe_json) == str:
            glencoe_json = json.loads(glencoe_json)

        video_json = {}
        for video in glencoe_json:
            # Get one of the URLs to compare with the xlink
            try:
                video_xlink =  glencoe_json[video]['ogv_href'].split('/')[-1].split('.')[0]
            except:
                video_xlink = None
            if video_xlink == self.xlink.split('.')[0]:
                video_json[video] = glencoe_json[video]
        
        if len(video_json) <= 0:
            return None
        else:
            return video_json
                    
    def glencoe_json(self):
        """
        Using this object DOI, contact Glencoe API for metadata
        """
        url = self.glencoe_metadata_url()
        if url is None:
            return None
        
        r = requests.get(url, allow_redirects=True)
        
        if r.status_code == requests.codes.ok:
            glencoe_json = r.json()
        else:
            glencoe_json = None
            
        return glencoe_json
    
    def glencoe_metadata_url(self):
        """
        Create the Glencoe metadata URL for an article
        """
        if self.get_doi() is None:
            return None
        
        url = self.glencoe_api_base_url + self.glencoe_metadata_endpoint + self.get_doi()
        return url