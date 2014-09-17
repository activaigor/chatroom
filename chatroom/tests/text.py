import tornado.httpserver
import tornado.ioloop
import tornado.web
import time

class TextHandler(tornado.web.RequestHandler):
    #@tornado.web.asynchronous
    def get(self):
        self.generator = self.generate_text(10)
        for i in self.generator:
            self.write(i)
        #tornado.ioloop.IOLoop.instance().add_callback(self.loop)

    def loop(self):
        try:
            text = self.generator.next()
            self.write(text)
            tornado.ioloop.IOLoop.instance().add_callback(self.loop)
        except StopIteration:
            self.finish()

    def generate_text(self, n):
        for x in xrange(n):
            time.sleep(0.5)
            if not x % 15:
                yield "FizzBuzz\n"
            elif not x % 5:
                yield "Buzz\n"
            elif not x % 3:
                yield "Fizz\n"
            else:
                yield "%s\n" % x