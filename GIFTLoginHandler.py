import tornado.web
import tornado.auth
import tornado.escape
import json

import pymongo
from pymongo import MongoClient
import uuid
import tornado.template 
from redmine import Redmine
from redmine.exceptions import AuthError

# route /redmine
class LoginHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.nextUrl = ""
	
	@tornado.gen.coroutine
	def post(self):
		if self.get_argument("nextUrl", None):
			self.nextUrl = self.get_argument("nextUrl")
		else:
			self.nextUrl = "http://tokyo.x-in-y.com:3000/"
		
		user = self.get_argument('user')
		passd = self.get_argument('pass')
		try:
			redmine_user = Redmine('http://tokyo.x-in-y.com:3000/', username=user, password=passd).auth()
			self.set_secure_cookie("user", tornado.escape.json_encode({'email': user+'@x-in-y.org'}))
			self.create_guid(user)
			self.redirect(self.get_argument("next", self.nextUrl))
		except AuthError as e:
			self.write('Error : {0}'.format(e.message))	

	@tornado.gen.coroutine
	def get(self):
		if self.get_argument("nextUrl", None):
			self.nextUrl = self.get_argument("nextUrl")
		else:
			self.nextUrl = "http://tokyo.x-in-y.com:3000/"
		if self.get_secure_cookie("user"):
			self.redirect(self.get_argument("next", self.nextUrl))
		else:
			self.render('redminelogin.html')
	
	def create_guid(self, user):
		email = user+'@x-in-y.com' # dummy email 
		#connection = pymongo.connection.Connection()
		#atlitepy = connection.atlitepy
		client = MongoClient()
		atlitepy = client.atlitepy
		users = atlitepy.users

		exists = users.find({"email":email})
		if exists.count() == 0:
			users.insert({"email":email,"user_guid":str(uuid.uuid4())})
