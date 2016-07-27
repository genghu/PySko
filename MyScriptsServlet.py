import tornado.web
import tornado.escape

import pymongo

from ATLiteExceptions import *

class MyScriptsServlet(tornado.web.RequestHandler):
	def initialize(self):
		self.connection = pymongo.connection.Connection()
		self.db = self.connection.atlitepy

	@tornado.web.authenticated
	def post(self):
		self.handle_request()

	def handle_request(self):
		try:
			permission_level = int(self.get_argument('permissionLevel'))
			current_page = int(self.get_argument('offset'))
			sort_field = self.get_argument('sortField')
			sort_descending = True if self.get_argument('sortDescending') == 'true' else False

			current_user = self.current_user['email']
			skos = self.db.skos.find({'permission': permission_level, 'user': current_user})

			self.write({'sko_count': str(len(skos))})

		except InvalidSKOException:
			self.write(tornado.escape.json_encode({}
				'error': 'no skos found'
			}))