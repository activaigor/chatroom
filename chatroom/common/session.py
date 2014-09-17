from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from tables import Users
import settings

class Session(object):

	__engine = None
	__session = None

	def __init__(self, sql_config):
		engine = self.engine_init(sql_config)
		self.__session = sessionmaker(bind = engine)

	@classmethod
	def instance(cls, sql_config):
		if not hasattr(cls, '__instance'):
			cls.__instance = cls(sql_config)
		return cls.__instance

	def get_session(self):
		return self.__session()

	def engine_init(self, sql_config):
		return create_engine(settings.SQL['db_uri'].format(**sql_config))
