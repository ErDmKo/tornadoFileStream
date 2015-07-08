import tornado.web

from tornado.testing import AsyncHTTPTestCase
from app.server import StreamHandler


class StreamTest(AsyncHTTPTestCase):
    def get_app(self):
        self.app = tornado.web.Application([('/', StreamHandler)])
        return self.app

    def simple_gereen_test(self):
        self.assertEqual(1, 1)
