from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class ProxyFailure(TestCase):
    def setUp(self):
        self.c = Client()

    def tearDown(self):
        pass

    def test_proxy_not_supported(self):
        "a request to anything beginning with '/proxy/' deliberately fails."
        resp = self.c.get(reverse("proxy"))
        self.assertEqual(resp.status_code, 404)
