import tornado.web
import os

from tornado.testing import AsyncHTTPTestCase
from app.server import StreamingHandler
from ._utils import encode_multipart_formdata, file_count


class StreamTest(AsyncHTTPTestCase):
    def setUp(self):
        super(StreamTest, self).setUp()
        for subdir, dirs, files in os.walk(StreamingHandler.UPLOAD_PATH):
            for fileInfo in files:
                os.remove(subdir+fileInfo)

    def get_app(self):
        self.app = tornado.web.Application([('/', StreamingHandler)])
        return self.app

    def test_simple_gereen(self):
        self.assertEqual(1, 1)

    def test_post(self):
        response = self.fetch('/', method="POST", body=b"")
        response.rethrow()
        self.assertEqual(response.code, 200)
        self.assertEqual(file_count(StreamingHandler.UPLOAD_PATH), 1)

    def test_post_file(self):
        with open('tests/test.pdf', 'rb') as upload_file:
            files = [(
                u'file',
                u'test.pdf',
                upload_file.read()
            )]
        content_type, body = encode_multipart_formdata(files)
        content_length = str(len(body))
        response = self.fetch(
            '/',
            method="POST",
            body=body,
            headers={
                "Content-Type": content_type,
                "Content-Length": content_length
            }
        )
        response.rethrow()
        self.assertEqual(response.code, 200)
        self.assertEqual(file_count(StreamingHandler.UPLOAD_PATH), 1)
