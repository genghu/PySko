import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import options, define
import tornado.ioloop

import ATLiteApplication

class ATLServer:
	def run(self):
		define("port", default=8889, type=int)
		tornado.options.parse_command_line()
		http_server = tornado.httpserver.HTTPServer(ATLiteApplication.ATLiteApplication())
		http_server.listen(options.port)
		ioloop = tornado.ioloop.IOLoop.instance()
		ioloop.start()

if __name__ == "__main__":
	atlserver = ATLServer()
	atlserver.run()