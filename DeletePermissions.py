import tornado.web
import tornado.escape

import pymongo

class DeletePermissions(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    def post(self):
        skoGuid = self.get_argument('skoGuid', None)
        email = self.get_argument('email', None)

        user = self.db.users.find_one({'email': email})
        userGuid = user['user_guid']

        self.db.permissions.remove({'guid': skoGuid, 'nickname': email})

        self.write(tornado.escape.json_encode({'success':'empty'}))