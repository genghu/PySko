import tornado.web
import tornado.escape

import urllib

import pymongo
import json

class SKOHistory(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    def get(self):
        skoGuid = self.get_argument('sko_id', None)
        action = self.get_argument('action', None)
        sko = self.db.skos.find_one({'skoGuid': skoGuid})
        #most_recent_history = self.db.skoScriptHistories.find({'skoGuid': skoGuid}).sort("updatedDate", pymongo.DESCENDING).limit(1)[0]
        history = self.db.history.find({'guid': skoGuid}).sort("timestamp", pymongo.DESCENDING)

        histories = []

        first = True
        recent_title = ''

        for h in history:
            user = self.db.users.find_one({'email': h['lastUpdatedBy']})
            histories.append(
                {
                    'title': urllib.unquote(h['title']),
                    'notes': urllib.unquote(h['notes']),
                    'historyGuid': h['historyGuid'],
                    'scriptContent': urllib.unquote(h['scriptContent']),
                    'updatedDate': h['timestamp'].strftime("%A, %B %d, %Y %H:%M:%S"),
                    'updatedBy': user['email']
                }
            )
            if first == True:
                recent_title = urllib.unquote(h['title'])
                first = False
    
        if action == None:
            self.render("SKOHistory.html", sko=sko, history=histories, skoGuid=skoGuid, title=recent_title)
        else:
            self.write(json.dumps(histories))
