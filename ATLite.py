import tornado.web
import tornado.escape

class ATLite(tornado.web.RequestHandler):
	@tornado.web.authenticated	
	def get(self):
		self.render('ATLite.html')

	def get_current_user(self):
		user = self.get_secure_cookie("user")
		if not user:
			return None
		return tornado.escape.json_decode(user)