import tornado.web
import tornado.escape

import pymongo

import uuid
import datetime

class ChangeDefaultHistory(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    def get(self):
        skoGuid = self.get_argument('skoGuid')
        historyGuid = self.get_argument('historyGuid')

        history = self.db.history.find_one({'guid':skoGuid, 'historyGuid':historyGuid })

        updatedHistory = {}
        updatedHistory['title'] = history['title']
        updatedHistory['notes'] = history['notes']
        updatedHistory['historyGuid'] = str(uuid.uuid4())
        updatedHistory['guid'] = skoGuid
        updatedHistory['scriptContent'] = history['scriptContent']
        updatedHistory['timestamp'] = datetime.datetime.now()
        updatedHistory['lastUpdatedBy'] = history['lastUpdatedBy']

        self.db.history.insert(updatedHistory)

        self.db.history.remove({'guid':skoGuid, 'historyGuid':historyGuid })

        self.redirect('/permissions?sko_id=%s' % (skoGuid))