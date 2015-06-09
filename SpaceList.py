import tornado.web

class SpaceList(tornado.web.RequestHandler):
    def get(self):
        self.write('<spaces><space value="fa" label="Free Association (by human)"/></spaces>')