import tornado.web
import tornado.escape
from uuid import uuid4
import pymongo

class RetrieveGuid(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    @tornado.web.authenticated
    def get(self):
        self.handle_request()

    def post(self):
        self.handle_request()

    def handle_request(self):
	email = self.current_user["email"]
        user = self.db.users.find_one({"email":email})

        self.write(tornado.escape.json_encode({"userGuid":user["user_guid"]}))

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return self.redirect("/realLogin?next=/getaccount")
        return tornado.escape.json_decode(user)
