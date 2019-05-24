from django.test import TestCase
from django.test.client import Client
from models import eLifeFile, MediaFile

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
            ('10.7554/eLife.03145', 'elife03145v001.AVI', 'mp4')
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
            
    def test_url_from_glencoe(self):
        "test parsing Glencoe API metadata and get the URL for a media file"
        
        # Result of
        # GET http://movie-usa.glencoesoftware.com/metadata/10.7554/eLife.00007
        json_string = ('{'
            + '"media-4":'
            + '    {"source_href": "http://static-movie-usa.glencoesoftware.com/source/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v004.AVI",'
            + '    "doi": "10.7554/eLife.00007.019",'
            + '    "flv_href": "http://static-movie-usa.glencoesoftware.com/flv/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v004.flv",'
            + '    "uuid": "b8fc244a-8f29-43de-a19f-85071ca11353",'
            + '    "title": "",'
            + '    "video_id": "media-4",'
            + '    "solo_href": "http://movie-usa.glencoesoftware.com/video/10.7554/eLife.00007/media-4",'
            + '    "height": 480,'
            + '    "ogv_href": "http://static-movie-usa.glencoesoftware.com/ogv/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v004.ogv",'
            + '    "width": 640,'
            + '    "href": "elife00007v004.AVI",'
            + '    "webm_href": "http://static-movie-usa.glencoesoftware.com/webm/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v004.webm",'
            + '    "jpg_href": "http://static-movie-usa.glencoesoftware.com/jpg/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v004.jpg",'
            + '    "duration": 45.478766999999998,'
            + '    "mp4_href": "http://static-movie-usa.glencoesoftware.com/mp4/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v004.mp4",'
            + '    "legend": "",'
            + '    "size": 54879232},'
            + '"media-1":'
            + '    {"source_href": "http://static-movie-usa.glencoesoftware.com/source/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v001.AVI",'
            + '     "doi": "10.7554/eLife.00007.016",'
            + '     "flv_href": "http://static-movie-usa.glencoesoftware.com/flv/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v001.flv",'
            + '     "uuid": "c7ea590e-941c-4834-8891-8a6601d49a2f",'
            + '     "title": "",'
            + '     "video_id": "media-1",'
            + '     "solo_href": "http://movie-usa.glencoesoftware.com/video/10.7554/eLife.00007/media-1",'
            + '     "height": 480,'
            + '     "ogv_href": "http://static-movie-usa.glencoesoftware.com/ogv/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v001.ogv",'
            + '     "width": 640,'
            + '     "href": "elife00007v001.AVI",'
            + '     "webm_href": "http://static-movie-usa.glencoesoftware.com/webm/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v001.webm",'
            + '     "jpg_href": "http://static-movie-usa.glencoesoftware.com/jpg/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v001.jpg",'
            + '     "duration": 46.579867,'
            + '     "mp4_href": "http://static-movie-usa.glencoesoftware.com/mp4/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v001.mp4",'
            + '     "legend": "",'
            + '     "size": 69605376},'
            + '"media-2":'
            + '    {"source_href": "http://static-movie-usa.glencoesoftware.com/source/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v002.AVI",'
            + '     "doi": "10.7554/eLife.00007.017",'
            + '     "flv_href": "http://static-movie-usa.glencoesoftware.com/flv/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v002.flv",'
            + '     "uuid": "34ac2c91-502b-46ce-a724-9585a7d3ce67",'
            + '     "title": "",'
            + '     "video_id": "media-2",'
            + '     "solo_href": "http://movie-usa.glencoesoftware.com/video/10.7554/eLife.00007/media-2",'
            + '     "height": 480,'
            + '     "ogv_href": "http://static-movie-usa.glencoesoftware.com/ogv/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v002.ogv",'
            + '     "width": 640,'
            + '     "href": "elife00007v002.AVI",'
            + '     "webm_href": "http://static-movie-usa.glencoesoftware.com/webm/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v002.webm",'
            + '     "jpg_href": "http://static-movie-usa.glencoesoftware.com/jpg/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v002.jpg",'
            + '     "duration": 40.006633000000001,'
            + '     "mp4_href": "http://static-movie-usa.glencoesoftware.com/mp4/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v002.mp4",'
            + '     "legend": "",'
            + '     "size": 67120640},'
            + '"media-3":'
            + '    {"source_href": "http://static-movie-usa.glencoesoftware.com/source/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v003.AVI",'
            + '     "doi": "10.7554/eLife.00007.018",'
            + '     "flv_href": "http://static-movie-usa.glencoesoftware.com/flv/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v003.flv",'
            + '     "uuid": "f4d6b37d-d5d6-4d85-bf27-0925bc3b0e20",'
            + '     "title": "",'
            + '     "video_id": "media-3",'
            + '     "solo_href": "http://movie-usa.glencoesoftware.com/video/10.7554/eLife.00007/media-3",'
            + '     "height": 480,'
            + '     "ogv_href": "http://static-movie-usa.glencoesoftware.com/ogv/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v003.ogv",'
            + '     "width": 640,'
            + '     "href": "elife00007v003.AVI",'
            + '     "webm_href": "http://static-movie-usa.glencoesoftware.com/webm/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v003.webm",'
            + '     "jpg_href": "http://static-movie-usa.glencoesoftware.com/jpg/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v003.jpg",'
            + '     "duration": 42.509132999999999,'
            + '     "mp4_href": "http://static-movie-usa.glencoesoftware.com/mp4/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v003.mp4",'
            + '     "legend": "",'
            + '     "size": 53251072}}')
            
        doi = '10.7554/eLife.00007'
        passes = [
            ('elife00007v001', 'mp4', 'http://static-movie-usa.glencoesoftware.com/mp4/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v001.mp4'),
            ('elife00007v002', 'jpg', 'http://static-movie-usa.glencoesoftware.com/jpg/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v002.jpg'),
            ('elife00007v003', 'webm', 'http://static-movie-usa.glencoesoftware.com/webm/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v003.webm'),
            ('elife00007v004', 'ogv', 'http://static-movie-usa.glencoesoftware.com/ogv/10.7554/102/c4dfcc6a0f187868c665d017428e6873ae4599bf/elife00007v004.ogv'),
            ]
        
        for args in passes:
            (xlink, type, url) = args
            m = MediaFile(doi, xlink, type)
            glencoe_url = m.get_url_from_glencoe(type, json_string)
            self.assertEqual(glencoe_url, url)
