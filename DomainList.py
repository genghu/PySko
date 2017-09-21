import tornado.web
import pymongo
from pymongo import MongoClient

class DomainList(tornado.web.RequestHandler):
    def initialize(self):
        #self.connection = pymongo.connection.Connection()
        #self.db = self.connection.dsspp
	self.client = MongoClient()
	self.db = client.dsspp
	
    def get(self):
        rows = self.db.domain_list.find({}, sort=[("number", pymongo.ASCENDING)])

        xml = '<domains>'
        for row in rows:
            xml += '<domain value="%s" label="%s"/>' % (row['label'], row['title'])
        xml += '</domains>'

        self.write(xml)
