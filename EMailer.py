import tornado.web
import tornado.escape

import pymongo

from gmail import GMailPy

from ATLiteExceptions import *

class EMailer(tornado.web.RequestHandler):
    def initialize(self):
        #self.connection = pymongo.connection.Connection()
        #self.db = self.connection.atlitepy
	self.client = MongoClient()
	self.db = client.atlitepy
        self.required_properties = ['userGuid', 'message', 'subject', 'to_addrs']

    def get(self):
        self.handle_request()

    def post(self):
        self.handle_request()

    def handle_request(self):
        try:
            json = self.json_in_request()
            properties = tornado.escape.json_decode(json)
            self.check_required_properties(properties)
            self.check_user_permissions(properties['userGuid'])

            g = GMailPy()
            for addr in properties['to_addrs'].split(','):
                if len(addr) > 0:
                    g.add_to_addr(addr.strip())
            g.set_subject(properties['subject'])
            g.set_message(properties['message'])
            g.send_message()

            self.write(tornado.escape.json_encode({'success':'sent'}))
        except JSONMissingError:
            self.write(tornado.escape.json_encode({'error':'no JSON found'}))
        except JSONPropertyMissingError, e:
            self.write(tornado.escape.json_encode({'error':e.message}))
        except PermissionDeniedError:
            self.write(tornado.escape.json_encode({'error':'invalid user GUID'}))

    def json_in_request(self):
        _json = self.get_argument('json', None)
        if _json is not None:
            return _json
        raise JSONMissingError()

    def check_user_permissions(self, userGuid):
        users = self.db.users
        user = users.find_one({'user_guid':userGuid})
        if user is None:
            raise PermissionDeniedError()

    def check_required_properties(self, props):
        for p in self.required_properties:
            try:
                check = props[p]
            except KeyError:
                raise JSONPropertyMissingError('property %s not found' % (p))
