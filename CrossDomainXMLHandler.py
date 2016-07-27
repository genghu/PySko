import tornado.web

class CrossDomain(tornado.web.RequestHandler):
	def get(self):
		self.handle_request()

	def post(self):
		self.handle_request()

	def handle_request(self):
		self.write('<cross-domain-policy><allow-access-from domain="*"/></cross-domain-policy>')