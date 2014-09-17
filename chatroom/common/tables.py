from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Users(Base):
	__tablename__ = 'users_table'
	id = Column(Integer, primary_key = True)
	name = Column(String, primary_key = True)
	passwd = Column(String)

	def __init__(self, **kwargs):
		map(lambda key: setattr(self, key, kwargs[key]), kwargs)

class Rooms(Base):
	__tablename__ = 'rooms'
	id = Column(Integer, primary_key = True)
	name = Column(String, primary_key = True)
	created = Column(DateTime, default = datetime.datetime.now)

	def __init__(self, **kwargs):
		map(lambda key: setattr(self, key, kwargs[key]), kwargs)

class UsersOnline(Base):
	__tablename__ = 'users_online'
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('users_table.id'))
	room_id = Column(Integer, ForeignKey('rooms.id'))

	def __init__(self, **kwargs):
		map(lambda key: setattr(self, key, kwargs[key]), kwargs)
