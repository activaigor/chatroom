import tornado.ioloop
import tornado.web
import settings
from handlers.login import LoginHandler
from handlers.signup import SignupHandler
from handlers.index import IndexHandler
from handlers.ajax import AjaxHandler
from handlers.base import BaseHandler
from handlers.jsonp import JsonpHandler
from handlers.rooms import RoomsHandler
from handlers.chat import ChatHandler
from common.tables import Users
from tests.text import TextHandler
import tornado.options

tornado.options.parse_command_line()

class MyApplication(tornado.web.Application):
    def __init__(self):
        settings = {
            "debug" : True,
            "cookie_secret" : "03ht]8B33c@^2opV1rDD2`mw3{T<?A",
            "login_url" : "/signin"
        }

        handlers = [
            (r"/", IndexHandler),
            (r"/signin", LoginHandler),
            (r"/signup", SignupHandler),
            (r"/test", TextHandler),
            (r"/ajax", AjaxHandler),
            (r"/chat", ChatHandler),
            (r"/jsonp", JsonpHandler),
            (r"/chat/(?P<room>[^/]+)", RoomsHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler,
                {'path' : 'static/'})
            #(r"/signup", RegisterHandler)
        ]
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    myapp = MyApplication()
    myapp.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()