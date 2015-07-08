import tornado.ioloop
import tornado.web
import os
from tornado import autoreload, websocket
import uuid
import tempfile, logging

class EchoWebSocket(websocket.WebSocketHandler):
    waiters = set()

    def open(self):
        EchoWebSocket.waiters.add(self)
        for subdir, dirs, files in os.walk('static/upload/'): 
            for fileInfo in files:
                EchoWebSocket.send_msg('/upload/'+fileInfo)

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        EchoWebSocket.waiters.remove(self)

    @classmethod
    def send_msg(cls, msg):
        for waiter in cls.waiters:
            try:
                waiter.write_message(msg)
            except:
                logging.error("Error sending message", exc_info=True)

@tornado.web.stream_request_body
class StreamingHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.bytes_read = 0

    def prepare(self):
        EchoWebSocket.send_msg('prepare')
        self.file_name = 'file_{0}'.format(uuid.uuid1().hex)
        self.fp = open('static/upload/{0}'.format(self.file_name), 'wb')
        self.max_length = int(self.request.headers.get('Content-Length'))
        self.request.connection.set_max_body_size(99999999999)
        self.request.connection.set_body_timeout(10000)

    def data_received(self, chunk):
        self.fp.write(chunk)
        self.bytes_read += len(chunk)
        EchoWebSocket.send_msg(str(self.bytes_read / self.max_length))

    def post(self):
        EchoWebSocket.send_msg('info')
        self.write('/upload/'+self.file_name)

if __name__ == "__main__":
    application = tornado.web.Application([
            (r"/tornado/upload/", StreamingHandler),
            (r"/tornado/ws/", EchoWebSocket),
        ])
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop().instance()
    autoreload.start(ioloop)
    tornado.ioloop.IOLoop.instance().start()
