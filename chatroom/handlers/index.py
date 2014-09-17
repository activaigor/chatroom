import tornado.web
import tornado.ioloop
from handlers.base import BaseHandler
from common.tables import Rooms

class IndexHandler(BaseHandler):

	def get_current_user(self):
	    return self.get_secure_cookie('user')
	
	@tornado.web.asynchronous
	@tornado.web.authenticated
	def get(self):
		tornado.ioloop.IOLoop.instance().add_callback(self.get_rooms)

	def get_rooms(self):
		db = self.session
		rooms = db.query(Rooms).all()
		template_data = {
			'user' : self.get_secure_cookie('user'),
			'rooms' : rooms
		}
		db.close()
		self.write(self.template.load('index.html').generate(**template_data))
		self.finish()
