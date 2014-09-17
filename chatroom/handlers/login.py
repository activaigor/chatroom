import tornado.web
import tornado.template
from settings import TEMPLATE_DIR
from handlers.base import BaseHandler
from common.tables import Users
import tornado.ioloop
import hashlib

class LoginHandler(BaseHandler):

	def get(self):
		self.write(self.template.load('signin.html').generate(success = None))

	@tornado.web.asynchronous
	def post(self):
		if self.get_argument('signup') is None:
			user = self.get_argument('user')
			passwd = hashlib.md5(self.get_argument('passwd').encode('utf-8')).hexdigest()
			tornado.ioloop.IOLoop.instance().add_callback(self.valid_data, user = user, passwd = passwd)
			print 'wait for valid'
		else:
			self.redirect('/signup')

	def valid_data(self, user, passwd):
		db = self.session
		data = db.query(Users).filter(Users.name == user).first()
		if data.passwd == passwd:
			self.set_secure_cookie('user', user)
			self.redirect('/')
		else:
			self.write(self.template.load('signin.html').generate(success = False))
			self.finish()

	def get_argument(self, argument):
		try:
			return super(LoginHandler, self).get_argument(argument)
		except tornado.web.MissingArgumentError:
			return None