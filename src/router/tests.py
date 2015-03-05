from django.test import TestCase
from django.test.client import Client
from models import *

class Routing(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_correct_redirects(self):
        "test valid parameters issue a 302 - temporary redirect response"
        passes = [
            ('a', '1'),
            
            ('ab', '1'),
            ('abc', '1'),
            ('zyx', '1'),
            
            ('a', '12'),
            ('a', '123'),
            ('a', '1234'),
            ('a', '12345'),
        ]
        for args in passes:
            try:
                url = '/v2/%s/%s/' % args
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302) # if you prefer
            except Exception:
                print('failed on',url)
                raise
            
    def test_incorrect_redirects(self):
        "test invalid params issue a 404 - not found response"
        fails = [
            # too many chars
            ('abcd', '1'),
            ('zyxw', '1'),

            # too many digits
            ('a', '123456'),
            ('a', '999999'),

            # too many chars and digits
            ('abcd', '123456'),

            # digits instead of chars
            ('1', '1'),

            # chars instead of digits
            ('a', 'a'),

            # digits instead of chars, chars instead of digits
            ('1', 'a')
        ]
        for args in fails:
            try:
                url = '/v2/%s/%s/' % args
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)
            except Exception:
                print('failed on',url)
                raise

    def test_correct_pdf(self):
        "test pdf file data"
        passes = [
            ('10.7554/eLife.00003'),
            ('10.7554/eLife.00003', 'figures'),
            ('00003'),
            ('00003', 'article'),
        ]
        for args in passes:
            try:
                if type(args) == tuple:
                    url = '/v2/articles/%s/pdf/%s' % args
                else:
                    url = '/v2/articles/%s/pdf' % args
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200) # if you prefer
            except Exception:
                print('failed on',args)
                raise
            
    def test_correct_media(self):
        "test media file data"
        passes = [
            ('10.7554/eLife.03145', 'elife03145v001', 'jpg'),
        ]
        for args in passes:
            try:
                if type(args) == tuple:
                    url = '/v2/articles/%s/media/%s/%s' % args
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200) # if you prefer
            except Exception:
                print('failed on',args)
                raise
            
class eLifeTestCase(TestCase):
    def setUp(self):
        self.elf = eLifeFile()

    def tearDown(self):
        pass
    
    def test_parse_s3_xml(self):
        "test parsing S3 object metadata XML"
        
        # Result of
        # GET http://s3.amazonaws.com/elife-cdn?prefix=elife-articles/00829/figures-pdf/elife00829-figures.pdf
        prefix = 'elife-articles/00829/figures-pdf/elife00829-figures.pdf'
        xml_string = ('<?xml version="1.0" encoding="UTF-8"?>'
                        + '<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                        + '<Name>elife-cdn</Name>'
                        + '<Prefix>elife-articles/00829/figures-pdf/elife00829-figures.pdf</Prefix>'
                        + '<Marker></Marker>'
                        + '<MaxKeys>1000</MaxKeys>'
                        + '<IsTruncated>false</IsTruncated>'
                        + '<Contents>'
                        + '<Key>elife-articles/00829/figures-pdf/elife00829-figures.pdf</Key>'
                        + '<LastModified>2015-01-29T23:50:00.000Z</LastModified>'
                        + '<ETag>&quot;82200c757af15dd8c0c85a39f74e4661&quot;</ETag>'
                        + '<Size>768145</Size>'
                        + '<StorageClass>STANDARD</StorageClass>'
                        + '</Contents>'
                        + '</ListBucketResult>')
        size = 768145
        
        s3_data = self.elf.parse_s3_xml(xml_string)
        
        self.assertEqual(size, s3_data[prefix]['size'])

    def test_correct_get_doi(self):
        "test get DOI"
        passes = [
            (3, '10.7554/eLife.00003'),
            ('03', '10.7554/eLife.00003'),
            ('00003', '10.7554/eLife.00003'),
            ('10.7554/eLife.00003', '10.7554/eLife.00003')
            ]
        
        for args in passes:
            self.elf.doi = args[0]
            self.assertEqual(self.elf.get_doi(), args[1])
        
    def test_correct_get_doi_id(self):
        "test get DOI id"
        passes = [
            (3, 3),
            ('03', 3),
            ('00003', 3),
            ('10.7554/eLife.00003', 3)
            ]
        
        for args in passes:
            self.elf.doi = args[0]
            self.assertEqual(self.elf.get_doi_id(), args[1])