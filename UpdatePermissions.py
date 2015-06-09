import tornado.web
import tornado.escape

import pymongo

class UpdatePermissions(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    def post(self):
        levelBefore = self.get_argument('levelBefore', None)
        levelAfter = self.get_argument('levelAfter', None)
        email = self.get_argument('email', None)
        skoGuid = self.get_argument('skoGuid', None)

        user = self.db.users.find_one({'email': email})
        userGuid = user['user_guid']

        self.db.skoPermissions.remove({
            'permission': int(levelBefore), 
            'nickname': email, 
            'guid': skoGuid
        })
        permission = {
            'permission': int(levelAfter),
            'nickname': nickname,
            'guid': skoGuid
        }
        self.db.skoPermissions.insert(permission)

        self.write(tornado.escape.json_encode({
            'level': int(permission['permission']),
            'nickname': permission['nickname'],
            'skoGuid': permission['guid'],
            'email': email
        }))