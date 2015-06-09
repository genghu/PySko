import tornado.web
import tornado.escape

import urllib

import pymongo

class RetrieveSKO(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    def get(self):
        self.handle_request()

    def post(self):
        self.handle_request()

    def handle_request(self):
        json = self.get_argument('json', None)
        if json is None:
            self.write(tornado.escape.json_encode({'error':'no JSON found'}))
            return
        properties = tornado.escape.json_decode(json)
        if not self.check_json_properties(properties):
            self.write(tornado.escape.json_encode({'error':'missing one or more JSON properties'}))
            return
        if not self.check_valid_sko(properties['guid']):
            self.write(tornado.escape.json_encode({'error':'sko guid is not valid'}))
            return
        if not self.check_user_permissions(properties['userGuid'], properties['guid']):
            self.write(tornado.escape.json_encode({'error':'user does not have at least viewer permissions'}))
            return
        self.write(tornado.escape.json_encode(self.get_sko(properties['guid'])))

    def get_sko(self, guid):
        # get sko 'metadata'
        skoScripts = self.db.skoScripts
        sko = skoScripts.find_one({'skoGuid':guid})
        skoScriptHistories = self.db.skoScriptHistories
        most_recent_history = skoScriptHistories.find().sort("updatedDate", pymongo.DESCENDING).limit(1)[0]

        return {
            'scriptType': sko['scriptType'],
            'resourceType': sko['resourceType'],
            'componentType': sko['componentType'],
            'resourceLocation': sko['resourceLocation'],
            'title': 'title',#self.unescape(most_recent_history['title']),#urllib.unquote(most_recent_history['title']),
            'notes': urllib.unquote(most_recent_history['notes']),
            'scriptContent': urllib.unquote(most_recent_history['scriptContent']),
            'guid': guid,
            'timestamp':most_recent_history['updatedDate'].strftime("%A, %B %d, %Y %H:%M:%S"),
            'published':sko['published'],
            'createdBy': self.get_user(most_recent_history['updatedBy'])
        }

    def get_user(self, guid):
        user = self.db.users.find_one({'user_guid': guid})
        return user['email']
        
    def check_json_properties(self, props):
        reqd_props = [
            'guid', 'userGuid'
        ]

        for p in reqd_props:
            try:
                check = props[p]
            except KeyError:
                return False

        return True

    def check_valid_sko(self, guid):
        skoScripts = self.db.skoScripts
        valid = skoScripts.find({'skoGuid':guid})
        return valid.count() > 0

    def check_user_permissions(self, userGuid, skoGuid):
        skoPermissions = self.db.skoPermissions
        permission = skoPermissions.find_one({'userGuid':userGuid, 'skoGuid':skoGuid})
        if permission is not None:
            return permission['level'] >= 1
        return False

    def unescape(self, script):
        script = re.sub("%u(..)(..)",r"\u\1\2",script)
        return urllib.unquote(script.decode('unicode_escape'))#urllib.unquote(script)
