import tornado.web
import tornado.auth
import tornado.escape

import pymongo
import uuid

class LoginHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
    def initialize(self):
        self.nextUrl = ""

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("nextUrl", None):
            self.nextUrl = self.get_argument("nextUrl")
        else:
            self.nextUrl = "/atlitepy"
            
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "auth failed")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        #create guid if needed
        self.create_guid(user)
        self.redirect(self.get_argument("next", self.nextUrl))

    def create_guid(self, user):
        email = user["email"]
        connection = pymongo.connection.Connection()
        atlitepy = connection.atlitepy
        users = atlitepy.users

        exists = users.find({"email":email})
        if exists.count() == 0:
            users.insert({"email":email,"user_guid":str(uuid.uuid4())})