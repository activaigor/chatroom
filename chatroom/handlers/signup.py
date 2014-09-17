import tornado.web
import tornado.template
import tornado.ioloop
from settings import TEMPLATE_DIR, SQL
from common.session import Session
from common.tables import Users
from handlers.base import BaseHandler
import hashlib
from sqlalchemy import exc

class SignupHandler(BaseHandler):

	def get(self):
		self.write(self.template.load('signup.html').generate(success = None))

	@tornado.web.asynchronous
	def post(self):
		if self.get_argument('register') is not None:
			user = self.get_argument('user')
			passwd = hashlib.md5(self.get_argument('passwd').encode('utf-8')).hexdigest()
        	tornado.ioloop.IOLoop.instance().add_callback(self.insert_data, user = user, passwd = passwd)

	def insert_data(self, user, passwd):
		db = self.session
		try:
			db.add(Users(name = user, passwd = passwd))
			db.commit()
			self.write(self.template.load('signup.html').generate(success = True))
		except Exception as e:
			db.rollback()
			db.close()
			self.write(self.template.load('signup.html').generate(success = False))
		finally:
			db.close()
			self.finish()

	def get_argument(self, argument):
		try:
			return super(SignupHandler, self).get_argument(argument)
		except tornado.web.MissingArgumentError:
			return None