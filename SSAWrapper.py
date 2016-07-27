import tornado.web
import tornado.escape

import pymongo

import SSA

from ATLiteExceptions import *

class SSAWrapper(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

        self.json = None

    def get(self):
        self.handle_request()

    def post(self):
        self.handle_request()

    def get_text(self):
        try:
            return self.json['text']
        except KeyError:
            return ''

    def get_cosine(self):
        try:
            return self.json['minStrength']
        except KeyError:
            return 0.0

    def get_weight(self):
        try:
            return self.json['minWeight']
        except KeyError:
            return 0.0

    def get_domains(self):
        try:
            return self.json['domains'].lower().split(' ')
        except KeyError:
            return 'combineall'

    def get_space(self):
        try:
            return self.json['SS']
        except KeyError:
            return 'fa'

    def get_rankby(self):
        try:
            return self.json['minRankby']
        except KeyError:
            return 0.0

    def get_wc(self):
        try:
            return self.json['wc']
        except KeyError:
            return 0.0

    def get_column_type(self):
        try:
            return self.json['type']
        except KeyError:
            return 0

    def get_category(self):
        try:
            return self.json['category']
        except KeyError:
            return 'general'

    def json_in_request(self):
        j = self.get_argument('json', None)
        if j is None:
            raise JSONMissingError()
        else:
            self.json = tornado.escape.json_decode(j)

    def check_required_properties(self):
        try:
            check = self.json['userGuid']
        except KeyError:
            raise JSONPropertyMissingError('user guid required')

    def validate_guid(self, guid):
        user = self.db.users.find_one({'user_guid':guid})
        if user is None:
            raise InvalidUserError()

    def handle_request(self):
        try:
            self.json_in_request()
            self.check_required_properties()
            self.validate_guid(self.json['userGuid'])

            ssa = SSA.SSA(
                self.get_text(),
                self.get_domains(),
                self.get_space(),
                self.get_column_type(),
                self.get_cosine(),
                self.get_weight(),
                self.get_rankby(),
                self.get_wc(),
                self.get_category()
            )
            self.write(tornado.escape.json_encode(ssa.query()))
        except JSONMissingError:
            self.write(tornado.escape.json_encode({'error':'JSON not found'}))
        except JSONPropertyMissingError, e:
            self.write(tornado.escape.json_encode({'error':e.message}))
        except InvalidUserError:
            self.write(tornado.escape.json_encode({'error':'invalid user guid'}))
