import tornado.web
import requests

from tornado.testing import AsyncHTTPTestCase
from app.server import StreamingHandler


class StreamTest(AsyncHTTPTestCase):

    def get_app(self):
        self.app = tornado.web.Application([('/', StreamingHandler)])
        return self.app

    def test_simple_gereen(self):
        self.assertEqual(1, 1)

    def test_post(self):
        response = requests.post(
            self.get_url('/'),
            files={'file': open('tests/test.pdf', 'r')},
            headers={
                'Content-Type': 'application/pdf'
            }
        )
        self.assertEqual(response.code, 200)
