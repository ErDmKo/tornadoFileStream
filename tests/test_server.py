import tornado.web

from tornado.testing import AsyncHTTPTestCase
from app.server import StreamingHandler


class StreamTest(AsyncHTTPTestCase):

    def get_app(self):
        self.app = tornado.web.Application([('/', StreamingHandler)])
        return self.app

    def test_simple_gereen(self):
        self.assertEqual(1, 1)

    def test_post(self):
        response = self.fetch('/', method="POST", body=b"")
        '''
            files={'file': open('tests/test.pdf', 'rb')},
            headers={
                'Content-Type': 'application/pdf'
            }
        )
        '''
        response.rethrow()
        self.assertEqual(response.code, 200)
