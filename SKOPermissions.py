import tornado.web
import tornado.escape

import urllib

import pymongo

from ATLiteExceptions import *

class SKOPermissions(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    @tornado.web.authenticated
    def get(self):
        skoGuid = self.get_argument('sko_id', None)
        if skoGuid==None:
            skoGuid = self.get_argument('guid', None)

        permissions = self.db.permissions.find({'guid': skoGuid})
        userGuid = self.db.users.find_one({'email':self.current_user['email']})['user_guid']
        most_recent_history = self.db.history.find({'guid': skoGuid}).sort("timestamp", pymongo.DESCENDING).limit(1)[0]
#        logfile = open('C:/atlskopermissiong.log', 'a')
#        print >> logfile, '******** %s' % (skoGuid)
#        logfile.close()
        skoCreatorPermission = self.db.permissions.find_one({'guid':skoGuid, 'permission':8})
        created_by = self.db.users.find_one({'email': skoCreatorPermission['nickname']})['email']
        updated_by = self.db.users.find_one({'email': most_recent_history['lastUpdatedBy']})['email']

        creators = []
        owners = []
        collaborators = []
        viewers = []

        userGuid = self.db.users.find_one({'email':self.current_user['email']})['user_guid']

        for p in permissions:
            if p['permission'] == 8:
                user = self.db.users.find_one({'email': p['nickname']})
                p['email'] = user['email']
                creators.append(p)
            if p['permission'] == 4:
                user = self.db.users.find_one({'email': p['nickname']})
                p['email'] = user['email']
                owners.append(p)
            if p['permission'] == 2:
                user = self.db.users.find_one({'email': p['nickname']})
                p['email'] = user['email']
                collaborators.append(p)
            if p['permission'] == 1:
                user = self.db.users.find_one({'email': p['nickname']})
                p['email'] = user['email']
                viewers.append(p)

        self.render('Details.html',#'SKOPermissions.html', 
            created = creators,
            owned = owners,
            collaborated = collaborators,
            viewable = viewers,
            skoDetails = {
                'userGuid': userGuid,
                'skoGuid': skoGuid,
                'title': urllib.unquote(most_recent_history['title']),
                'notes': self.strip_cdata(urllib.unquote(most_recent_history['notes'])),
                'last_updated': most_recent_history['timestamp'].strftime("%A, %B %d, %Y %H:%M:%S"),
                'created_by': created_by,
                'updated_by': updated_by,
                'nickname': self.current_user['email']
            } 
        )

    def strip_cdata(self, d):
        d = d[9:]
        d = d[:len(d)-3]
        return d

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return None
        return tornado.escape.json_decode(user)
