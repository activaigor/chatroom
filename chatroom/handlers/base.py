import tornado.web
from common.session import Session
import tornado.websocket
import tornado.template
from settings import TEMPLATE_DIR, SQL

class BaseHandler(tornado.web.RequestHandler):
	@property
	def session(self):
		instance = Session.instance(SQL['heroku'])
		return instance.get_session()

	@property
	def template(self):
		template = tornado.template.Loader(TEMPLATE_DIR)
		return template

class WebSocketBaseHandler(tornado.websocket.WebSocketHandler):
	@property
	def session(self):
		instance = Session.instance(SQL['heroku'])
		return instance.get_session()