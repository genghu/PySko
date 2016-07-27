import tornado.web
import tornado.escape

from ATLiteExceptions import *

import pymongo

class CheckPermission(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    def get(self):
        self.handle_request()

    def post(self):
        self.handle_request()

    def handle_request(self):
        self.write(tornado.escape.json_encode({'permissionExists':True}))
        """
        try:
            json = self.json_in_request()
            properties = tornado.escape.json_decode(json)
            self.check_required_properties(properties)
            self.check_valid_sko(properties['guid'])
            self.check_user_permissions(properties['userGuid'], properties['guid'],properties['permission'])
            self.write(tornado.escape.json_encode({'permissionExists':True}))

        except JSONMissingError:
            self.write(tornado.escape.json_encode({'error':'no JSON found'}))
        except JSONPropertyMissingError, e:
            self.write(tornado.escape.json_encode({'error':e.message}))
        except PermissionDeniedError:
            self.write(tornado.escape.json_encode({'permissionExists':False}))
        except InvalidSKOError:
            self.write(tornado.escape.json_encode({'error':'SKO not found'}))
        """

    def check_valid_sko(self, guid):
        skoScripts = self.db.skoScripts
        sko = skoScripts.find_one({'skoGuid':guid})
        if sko is None:
            raise InvalidSKOError()

    def check_user_permissions(self, userGuid, skoGuid, level):
        skoPermissions = self.db.skoPermissions
        permission = skoPermissions.find_one({'userGuid':userGuid, 'skoGuid':skoGuid})
        if permission is None:
            raise PermissionDeniedError()
        if permission['level'] < level:
            raise PermissionDeniedError()

    def json_in_request(self):
        _json = self.get_argument('json', None)
        if _json is not None:
            return _json
        raise JSONMissingError()

    def check_required_properties(self, props):
        reqd_props = [
            'guid', 'userGuid', 'permission'
        ]

        for p in reqd_props:
            try:
                check = props[p]
            except KeyError:
                raise JSONPropertyMissingError('property %s not found' % (p))