import tornado.web
import tornado.escape

import pymongo

class TrashSKO(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    def post(self):

        #objectid = self.get_argument('objectid',None)
        skoGuid = self.get_argument('guid',None)
        action = self.get_argument('action',None)
        if skoGuid != None:

            p = self.db.permissions.find({"guid":skoGuid})
            for q in p:
                if action=="trash":
                    self.db.permissions.update({"_id":q['_id']}, {'$set':{"inTrash":1}}, True)
                else:
                    if action == "restore":
                        self.db.permissions.update({"_id":q['_id']}, {'$set':{"inTrash":0}}, True)

            