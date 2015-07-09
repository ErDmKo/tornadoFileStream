import tornado.ioloop
import tornado.web
import os
from tornado import autoreload, websocket
import uuid


@tornado.web.stream_request_body
class StreamingHandler(tornado.web.RequestHandler):
    UPLOAD_URL = '/upload/'
    UPLOAD_PATH = 'static' + UPLOAD_URL

    def initialize(self):
        self.bytes_read = 0

    def prepare(self):
        EchoWebSocket.send_msg('prepare')
        self.file_name = 'file_{0}'.format(uuid.uuid1().hex)
        self.fp = open(
            '{0}{1}'.format(self.UPLOAD_PATH, self.file_name),
            'wb'
        )
        self.max_length = int(self.request.headers.get('Content-Length'))
        self.request.connection.set_max_body_size(99999999999)
        self.request.connection.set_body_timeout(10000)

    def data_received(self, chunk):
        self.fp.write(chunk)
        self.bytes_read += len(chunk)
        EchoWebSocket.send_msg(str(self.bytes_read / self.max_length))

    def post(self):
        EchoWebSocket.send_msg('info')
        self.write(self.UPLOAD_URL+self.file_name)


class EchoWebSocket(websocket.WebSocketHandler):
    waiters = set()

    def open(self):
        EchoWebSocket.waiters.add(self)
        for subdir, dirs, files in os.walk(StreamingHandler.UPLOAD_PATH):
            for fileInfo in files:
                EchoWebSocket.send_msg(StreamingHandler.UPLOAD_URL+fileInfo)

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        EchoWebSocket.waiters.remove(self)

    @classmethod
    def send_msg(cls, msg):
        for waiter in cls.waiters:
            waiter.write_message(msg)

if __name__ == "__main__":
    application = tornado.web.Application([
            (r"/tornado/upload/", StreamingHandler),
            (r"/tornado/ws/", EchoWebSocket),
        ])
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop().instance()
    autoreload.start(ioloop)
    tornado.ioloop.IOLoop.instance().start()
