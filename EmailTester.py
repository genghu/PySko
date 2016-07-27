import tornado.web
import tornado.httpclient
import tornado.escape

import urllib

class EmailTester(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        json = {}
        json['userGuid'] = "4d1f7969-d202-4ffb-869e-a952d636113d"
        json['to_addrs'] = "faisal_cse_03@yahoo.com,iFaisalRahman@gmail.com,faisalbuet03@gmail.com"
        json['subject'] = "Test Python"
        json['message'] = "This is so Python"
        
        request = tornado.httpclient.HTTPRequest(
            url='http://localhost:8888/emailer',
            method='POST',
            body=urllib.urlencode({"json":tornado.escape.json_encode(json)})
        )
        http.fetch(request, callback=self.on_response)
        self.finish()

    def on_response(self, response):
        pass