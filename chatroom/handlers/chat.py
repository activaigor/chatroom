import tornado.web
import tornado.ioloop
from handlers.base import WebSocketBaseHandler
from common.tables import UsersOnline, Users, Rooms
import json
import re
import requests
from bs4 import BeautifulSoup
import random

re_http = re.compile(r'^(https?://\S+)')
re_title = re.compile(r'<title>(.+)</title>')
re_div = re.compile(r'<div.*>(.+)</div>', re.S)
re_img = re.compile(r'(<img.*>)', re.S)
re_description = re.compile(r'<description>(.+)</description>')
users = []

class ChatHandler(WebSocketBaseHandler):

	def open(self):
		users.append(self)

	@tornado.web.asynchronous
	def on_message(self, message):
		msg = json.loads(message)
		username = self.get_secure_cookie('user')
		if msg['type'] == 'hello':
			self.__add_user(msg)
			msg['type'] = 'user'
			msg['from'] = 'system'
			msg['body'] = username + ' connected to chat'
			for user in users:
				user.write_message(json.dumps(msg))
		elif msg['type'] == 'user':
			match = re_http.findall(msg['body'])
			if len(match) > 0:
				url = str(match[0]) if str(match[0])[-1] == '/' else str(match[0]) + '/'
				r = requests.get(url)
				soup = BeautifulSoup(r.text)
				msg['body'] = str(random.choice(soup.find_all('img')).encode('utf-8'))
				msg['body'] = msg['body'].join([str(random.choice(soup.find_all('div')).encode('utf-8')) for i in range(0,2)])
				msg_attr = {
					'favicon' : '<img src="' + url + 'favicon.ico">',
					'body' : msg['body'],
					'url' : url,
					'title' : '<h3>' + str(soup.title.string.encode('utf-8')) + '</h3>'
				}
				msg['body'] = '{favicon}<a href="{url}">{url}</a><div id="site_preview">{title}{body}</div>'.format(**msg_attr)
				message = json.dumps(msg)
			for user in users:
				user.write_message(message)


	def on_close(self):
		username = self.get_secure_cookie('user')
		self.__del_user(username)
		users.remove(self)
		msg = {
			'type' : 'user',
			'from' : 'system',
			'room' : 'all',
			'body' : username + ' leave the chat'
		}
		for user in users:
			user.write_message(json.dumps(msg))

	def __del_user(self, user):
		db = self.session
		usr = db.query(UsersOnline).join(Users).filter(Users.name == user).first()
		if usr is not None:
			db.delete(usr)
		try:
			db.commit()
		except Exception as e:
			db.rollback()
			db.close()
		finally:
			db.close()

	def __add_user(self, msg):
		db = self.session
		room = db.query(Rooms).filter(Rooms.name == msg['room']).first()
		user = db.query(Users).filter(Users.name == msg['from']).first()
		db.add(UsersOnline(user_id = user.id, room_id = room.id))
		try:
			db.commit()
		except Exception as e:
			db.rollback()
			db.close()
		finally:
			db.close()