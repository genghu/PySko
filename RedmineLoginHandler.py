#https://github.com/joestump/python-oauth2

import tornado.web
import tornado.auth
import tornado.escape
import json
from torndsession import sessionhandler

import pymongo
from uuid import uuid4
import tornado.template 
import urllib 
import urlparse
import oauth2 as oauth
import pprint

REDIRECT_URI = "http://ccnu.x-in-y.com:8889/redmineCallback"

# Create your consumer with the proper key/secret.
consumer_key="rfszuzHlfUaa5D5n4cLGUwLMV8mWn7HAii1VuxBI" 
consumer_secret="IPuZtbSq4dge35W5hjTvO5B7I5EKvpdjDDKM5Fvo"

consumer = oauth.Consumer(consumer_key, consumer_secret)

# Request token URL for Twitter.
request_token_url = "http://ccnu.x-in-y.com:3000/oauth/request_token"
access_token_url = 'http://ccnu.x-in-y.com:3000/oauth/access_token'
authorize_url = 'http://ccnu.x-in-y.com:3000/oauth/authorize'
userinfo_url = 'http://ccnu.x-in-y.com:3000/oauth/user_info'
currentuser_url = 'http://ccnu.x-in-y.com:3000/oauth/current_user'
test_url = 'http://ccnu.x-in-y.com:3000/oauth/test_url'
uloggedin_url = 'http://ccnu.x-in-y.com:3000/oauth/user_logged_in'


#class Main(tornado.web.RequestHandler):
class Main(sessionhandler.SessionBaseHandler):
	def initialize(self):
		self.nextUrl = ""
		self.state = ""	

	@tornado.gen.coroutine
	def get(self):
		if self.get_argument("nextUrl", None):
			self.nextUrl = self.get_argument("nextUrl")
		else:
			self.nextUrl = "http://www.auto-tutor.com/1024768/general/author.html"
	    		#self.nextUrl = 'http://ccnu.x-in-y.com:8889/list_skos' 
		#check if we have access_token, otherwise we need to have one thru redmine oauth	
		if 'access_token' in self.session and self.session['access_token']:
			self.redirect(self.get_argument("next", self.nextUrl))
		
		else:
			client = oauth.Client(consumer)
  	        	resp, content = client.request(request_token_url, "GET")
			if resp['status'] != '200':
    				raise Exception("Invalid response %s." % resp['status'])

			request_token = dict(urlparse.parse_qsl(content))
    			#store it for later use
			self.session['request_token'] = request_token

			url = authorize_url+'?oauth_token='+request_token['oauth_token']
			#self.render('testmain.html', rt = request_token,url=url)
			self.redirect(url)
	
#class Callback(tornado.web.RequestHandler):
class Callback(sessionhandler.SessionBaseHandler):
	def initialize(self):
		self.nextUrl = ""
	
	@tornado.gen.coroutine
	#def get(self):
	def get(self):
		if self.get_argument("nextUrl", None):
			self.nextUrl = self.get_argument("nextUrl")
		else:
			self.nextUrl = "http://www.auto-tutor.com/1024768/general/author.html"
		
		request_token = self.session['request_token']

		oauth_verifier = self.get_argument('oauth_verifier')
                token = oauth.Token(
				request_token['oauth_token'],
 				request_token['oauth_token_secret'])
		token.set_verifier(oauth_verifier)
		client = oauth.Client(consumer,token)
		resp, content = client.request(access_token_url, "POST")
		if resp['status'] != '200':
    			raise Exception("Invalid response %s." % resp['status'])
		access_token = dict(urlparse.parse_qsl(content))
		self.session['access_token'] = access_token 

		# find out who is logged it and get his/her email id 	
		resp, content = client.request(uloggedin_url+'?access_token='+access_token['oauth_token'], "GET")
		if resp['status'] != '200':
    			raise Exception("Invalid response %s." % resp['status'])
                # found the email 
	        email = content 
                print email 
                self.create_guid(email)
		email = tornado.escape.json_encode({'email': email})
 	        self.set_secure_cookie("user", email)
		self.redirect(self.get_argument("next", self.nextUrl))
	
	def create_guid(self, email):
		connection = pymongo.connection.Connection()
		atlitepy = connection.atlitepy
		users = atlitepy.users
		
		exists = users.find({"email":email})
		if exists.count() == 0:
		    users.insert({"email":email,"user_guid":str(uuid4())})	
