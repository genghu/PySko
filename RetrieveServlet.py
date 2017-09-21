import tornado.web
import tornado.escape
import re

import pymongo
from pymongo import MongoClient

from PermissionManager import PermissionManager

from ATLiteExceptions import *

import urllib

class RetrieveServlet(tornado.web.RequestHandler):
    def initialize(self):
        self.pm = PermissionManager()
        #self.connection = pymongo.connection.Connection()
        #self.db = self.connection.atlitepy
	self.client = MongoClient()
	self.db = client.atlitepy

    #@tornado.web.authenticated
    def get(self):
        self.handle_request()

    #@tornado.web.authenticated
    def post(self):
        self.handle_request()

    def handle_request(self):
        try:
            json = self.get_argument("json", None)
            jsonObject = tornado.escape.json_decode(json)
            guid = jsonObject['guid']
            """
            source = jsonObject['source']
            if source == 'authoringtool':
                currentNickname = self.current_user['email']
                if not self.pm.checkPermission(currentNickname, guid, 2):
                    self.write(tornado.escape.json_encode({
                        'error': 'No edit permissions'
                    }))
                    return
            """

            return_back = None

            try:
                return_back = jsonObject['return']
            except KeyError, e:
                pass
            
            scriptObject = self.getSKOScriptByGUID(guid)
            mostRecentHistory = self.getMostRecentHistory(guid)
            scriptObject['scriptContent'] = self.unescape(mostRecentHistory['scriptContent'])
            scriptObject['timestamp'] = scriptObject['timestamp'].strftime("%A, %B %d, %Y %H:%M:%S")
            scriptObject['_id'] = str(scriptObject['_id'])
            scriptObject['componentType'] = urllib.unquote(scriptObject['componentType'])
            scriptObject['resourceType'] = urllib.unquote(scriptObject['resourceType'])
            scriptObject['resourceLocation'] = urllib.unquote(scriptObject['resourceLocation'])
            scriptObject['title'] =self.unescape(scriptObject['title'])
            scriptObject['scriptType'] = urllib.unquote(scriptObject['scriptType'])
            scriptObject['notes'] = urllib.unquote(scriptObject['notes'])
            if return_back is None:
                self.write(tornado.escape.json_encode(scriptObject))
            else:
                self.write(scriptObject[return_back])
            
        except InvalidSKOError:
            self.write(tornado.escape.json_encode({
                'error': 'GUID not found'
            }))

    def getSKOScriptByGUID(self, guid):
        skos = self.db.skos.find({'guid': guid})
        if skos.count() > 0:
            return skos[0]
        raise InvalidSKOError()

    def getMostRecentHistory(self, guid):
        most_recent_history = self.db.history.find({'guid': guid}).sort("timestamp", pymongo.DESCENDING).limit(1)[0]
        return most_recent_history

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return None
        return tornado.escape.json_decode(user)

    def unescape(self, script):
        script = re.sub("%u(..)(..)",r"\u\1\2",script)
        return urllib.unquote(script.decode('unicode_escape'))#urllib.unquote(script)

