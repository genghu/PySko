import tornado.web
import tornado.escape

from RetrieveAccount import RetrieveAccount

import urllib
import json

class RetrieveAccountWrapper(tornado.web.RequestHandler):
    def initialize(self):
        self.retrieveAccount = None

    @tornado.web.authenticated
    def get(self):
        self.handleRequest()

    @tornado.web.authenticated
    def post(self):
        self.handleRequest()

    def handleRequest(self):


        action = self.get_argument("action", None)
        preference = self.get_argument("preference",None)
        preference_title = self.get_argument("preferenceTitle",None)
        name = self.get_argument("name",None)
        timestamp = self.get_argument("timestamp",None)
        profile_id = self.get_argument("profileID",None)
        show_all=self.get_argument("showAll",None)


        name = self.current_user["email"]

        print action
        
        self.retrieveAccount = RetrieveAccount(action,name, preference, preference_title, timestamp ,profile_id,show_all)
        results = self.retrieveAccount.go()

        if action == "create":
            self.write(results)
        else:
            if action == "update":
                self.write(results)
            else:
                self.write(urllib.unquote((str(results)).decode('unicode_escape')))

    def get_current_user(self):

        user = self.get_secure_cookie("user")
        if not user:
            return None
        return tornado.escape.json_decode(user)