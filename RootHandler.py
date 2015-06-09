import tornado.web
import tornado.escape

class RootHandler(tornado.web.RequestHandler):
    @tornado.web.authenticated
    def get(self):
        if self.is_authenticated():
            login_name = tornado.escape.xhtml_escape(self.current_user["email"])
            self.write(login_name)
        else:
            self.redirect("/login")

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)

    def is_authenticated(self):
        return self.get_current_user() != None