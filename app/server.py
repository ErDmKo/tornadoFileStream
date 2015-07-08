import tornado.ioloop
import tornado.web


@tornado.web.stream_request_body
class StreamHandler(tornado.web.RequestHandler):

    def post(self):
        pass

if __name__ == "__main__":
    application = tornado.web.Application([
            (r"/", StreamHandler),
        ])
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
