import tornado.web
import tornado.ioloop
from common.tables import UsersOnline, Users
from handlers.base import BaseHandler

class RoomsHandler(BaseHandler):

	def get_current_user(self):
	    return self.get_secure_cookie('user')
	
	@tornado.web.authenticated
	@tornado.web.asynchronous
	def get(self, room):
		user = self.get_current_user()
		tornado.ioloop.IOLoop.instance().add_callback(self.get_users_online, user = user, room = room)

	def get_users_online(self, user, room):
		db = self.session
		users = db.query(Users).join(UsersOnline).all()
		db.close()
		self.write(self.template.load('chat.html').generate(user = user, chat_room = room, users = users))
		self.finish()