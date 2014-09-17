import tornado.ioloop
import tornado.web
from common.tables import Rooms, Users, UsersOnline
from handlers.base import BaseHandler
import json

class AjaxHandler(BaseHandler):

	def get(self):
		self.redirect('/')

	@tornado.web.asynchronous
	def post(self):
		if self.get_argument('room_add') is not None:
			name = self.get_argument('name')
			tornado.ioloop.IOLoop.instance().add_callback(self.room_add, name = name)
			print 'waiting for adding'
		elif self.get_argument('users_online') is not None:
			tornado.ioloop.IOLoop.instance().add_callback(self.get_users_online)
			print 'waiting for online results'

	def get_users_online(self):
		db = self.session
		users = db.query(Users).join(UsersOnline).all()
		db.close()
		response = {
			'success' : True,
			'data' : [user.name for user in users]
		}
		self.write(json.dumps(response))
		self.finish()

	def room_add(self, name):
		db = self.session
		try:
			db.add(Rooms(name = name))
			db.commit()
			print 'ok'
		except Exception as e:
			print e
			db.rollback()
			db.close()
		finally:
			db.close()
			self.write(json.dumps({'success' : True}))
			self.finish()

	def get_argument(self, argument):
		try:
			return super(AjaxHandler, self).get_argument(argument)
		except tornado.web.MissingArgumentError:
			return None
