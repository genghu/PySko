import tornado.web
import tornado.auth
import tornado.escape
import json

import pymongo
import uuid

# route /google
class LoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleOAuth2Mixin):
	def initialize(self):
		self.nextUrl = ""

	@tornado.gen.coroutine
	def get(self):
		if self.get_argument("nextUrl", None):
			self.nextUrl = self.get_argument("nextUrl")
		else:
			self.nextUrl = "http://www.skoonline.org/s-k-o/ccnuserver"

		if self.get_argument('code', False):
			user = yield self.get_authenticated_user(redirect_uri='http://ccnu.x-in-y.com:8889/oauth2callback', code=self.get_argument('code'))
            # Save the user with e.g. set_secure_cookie
			if not user:
				raise tornado.web.HTTPError(500, "Google auth failed")
			access_token = str(user['access_token'])
			http_client = self.get_auth_http_client()
			response =  yield http_client.fetch('https://www.googleapis.com/oauth2/v1/userinfo?access_token='+access_token)
			if not response:
				self.clear_all_cookies() 
				raise tornado.web.HTTPError(500, 'Google auth failed')
			user = json.loads(response.body)
			self.set_secure_cookie("user", tornado.escape.json_encode(user))
			# create guid if needed
			self.create_guid(user)
			self.redirect(self.get_argument("next", self.nextUrl))
		else:
			yield self.authorize_redirect( redirect_uri='http://ccnu.x-in-y.com:8889/oauth2callback', client_id=self.settings['google_oauth']['key'], scope=['email'], response_type='code', extra_params={'approval_prompt': 'auto'})

	def create_guid(self, user):
		email = str(user["email"])
		connection = pymongo.connection.Connection()
		atlitepy = connection.atlitepy
		users = atlitepy.users

		exists = users.find({"email":email})
		if exists.count() == 0:
			users.insert({"email":email,"user_guid":str(uuid.uuid4())})
