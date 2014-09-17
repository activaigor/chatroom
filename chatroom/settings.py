PORT = 5000
TEMPLATE_DIR = 'chatroom/templates'

SQL = dict(
	db_uri = 'postgres://{user}:{pasw}@{host}:{port}/{data}',
	heroku = dict(
			host = 'ec2-54-83-43-49.compute-1.amazonaws.com',
			port = '5432',
			user = 'qetxaijgzmpbzi',
			pasw = 'Y-c4N56681GgE3-stOTQJ7SN3Y',
			data = 'd53kkgjq3l22j5'
		)
)