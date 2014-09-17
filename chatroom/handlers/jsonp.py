import tornado.ioloop
import tornado.web
from common.tables import Rooms
from handlers.base import BaseHandler
import json

class JsonpHandler(BaseHandler):

	@tornado.web.asynchronous
	def get(self):
		room = self.get_argument('term')
		if room is not None:
			tornado.ioloop.IOLoop.instance().add_callback(self.room_search, room = room)

	def room_search(self, room):
		db = self.session
		rooms = db.query(Rooms).filter(Rooms.name.like('%' + room + '%')).all()
		db.close()
		if rooms is not None:
			result = [i.name for i in rooms]
			self.write(json.dumps(result))
		self.finish()

	def get_argument(self, argument):
		try:
			return super(JsonpHandler, self).get_argument(argument)
		except tornado.web.MissingArgumentError:
			return None
