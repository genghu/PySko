import tornado.web
import tornado.escape

# route /login
class LoginServlet(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.handle_request()

    def post(self):
        self.handle_request()

    def handle_request(self):
        current_user = self.current_user
        from_user = self.get_argument('from_user', None)
        next = self.get_argument('next', None)
        loginUrl = '/realLogin'
        if next is not None:
            loginUrl += '?next=' + next
        

        if current_user is None:
            if from_user is None:
                self.write(tornado.escape.json_encode({
                    'error': 'No user logged in',
                    'loginUrl': loginUrl
                }))
            else:
                self.redirect('/realLogin')
        else:
            self.write(tornado.escape.json_encode({
                'nickname': self.current_user['email']
            }))

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return None
        return tornado.escape.json_decode(user)
