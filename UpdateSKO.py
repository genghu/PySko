import tornado.web
import tornado.escape

from ATLiteExceptions import *

import pymongo
import datetime
import uuid

class UpdateSKO(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy
        self.updateable_properites = ['title', 'notes', 'scriptContent', 'published']

    def get(self):
        self.handle_request()

    def post(self):
        self.handle_request()

    def handle_request(self):
        try:
            json = self.json_in_request()
            properties = tornado.escape.json_decode(json)
            self.check_required_properties(properties)
            self.check_valid_sko(properties['skoGuid'])
            self.check_user_permissions(properties['userGuid'], properties['skoGuid'])

            updated_properties = [p for p in properties if p not in ['userGuid', 'skoGuid']]

            if len(updated_properties) > 0:

                most_recent_history = self.db.skoScriptHistories.find({'skoGuid': properties['skoGuid']}).sort("updatedDate", pymongo.DESCENDING).limit(1)[0]
                new_history = {
                    'title': most_recent_history['title'],
                    'notes': most_recent_history['notes'],
                    'skoGuid':most_recent_history['skoGuid'],
                    'scriptContent': most_recent_history['scriptContent'],
                    'updatedBy':properties['userGuid'],
                    'updatedDate':datetime.datetime.now(),
                    'historyGuid':str(uuid.uuid4())
                }

                for p in updated_properties:
                    if p in self.updateable_properites:
                        new_history[p] = properties[p]

                self.db.skoScriptHistories.insert(new_history)

            self.write(tornado.escape.json_encode({'skoGuid':properties['skoGuid']}))          
            

        except JSONMissingError:
            self.write(tornado.escape.json_encode({'error':'no JSON found'}))
        except JSONPropertyMissingError, e:
            self.write(tornado.escape.json_encode({'error':e.message}))
        except PermissionDeniedError:
            self.write(tornado.escape.json_encode({'error':'user must have at least collaborator permissions to edit SKO'}))
        except InvalidSKOError:
            self.write(tornado.escape.json_encode({'error':'SKO not found'}))

    def check_valid_sko(self, guid):
        skoScripts = self.db.skoScripts
        sko = skoScripts.find_one({'skoGuid':guid})
        if sko is None:
            raise InvalidSKOError()

    def check_user_permissions(self, userGuid, skoGuid):
        skoPermissions = self.db.skoPermissions
        permission = skoPermissions.find_one({'userGuid':userGuid, 'skoGuid':skoGuid})
        if permission is None:
            raise PermissionDeniedError()
        if permission['level'] < 2:
            raise PermissionDeniedError()

    def json_in_request(self):
        _json = self.get_argument('json', None)
        if _json is not None:
            return _json
        raise JSONMissingError()

    def check_required_properties(self, props):
        reqd_props = [
            'userGuid', 'skoGuid'
        ]

        for p in reqd_props:
            try:
                check = props[p]
            except KeyError:
                raise JSONPropertyMissingError('property %s not found' % (p))