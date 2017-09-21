import tornado.web
import tornado.escape

import pymongo

class DeleteSKOByAdmin(tornado.web.RequestHandler):
    def initialize(self):
        #self.connection = pymongo.connection.Connection()
        #self.db = self.connection.atlitepy
	self.client = MongoClient()
	self.db = client.atlitepy

    def get(self):

        #objectid = self.get_argument('objectid',None)
        skoGuid = self.get_argument('guid',None)
        #action = self.get_argument('action',None)
        if skoGuid != None:
            
            p = list(self.db.skos.find({"guid":skoGuid}))
            if len(p)==0:
                self.write( "{\"error\":\"Script with GUID not found\"}")
            for q in p:
                self.db.skos.remove({"_id":q["_id"]})

            p = list(self.db.permissions.find({"guid":skoGuid}))
            for q in p:
                self.db.permissions.remove({"_id":q["_id"]})

            p = list(self.db.history.find({"guid":skoGuid}))
            for q in p:
                self.db.history.remove({"_id":q["_id"]})                


            self.write( "{\"complete\":\"complete\"}")

            
