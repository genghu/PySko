import tornado.web
import tornado.escape

import pymongo

from pymongo import MongoClient

import Base

from ATLiteExceptions import *

class BaseWrapper(tornado.web.RequestHandler):
    def initialize(self):
        self.json = None

        #self.connection = pymongo.connection.Connection()
        #self.db = self.connection.atlitepy
	self.client = MongoClient()
	self.db = client.atlitepy

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

    def get_etop(self):
        try:
            return self.json['etop']
        except KeyError:
            return 5

    def get_ttop(self):
        try:
            return self.json['ttop']
        except KeyError:
            return 5

    def get_format(self):
        try:
            return self.json['format']
        except KeyError:
            return 'xml'

    def get_domain(self):
        try:
            return self.json['domain']
        except KeyError:
            return 'combineall'

    def get_space(self):
        try:
            return self.json['SS']
        except KeyError:
            return 'tasalsa'

    def get_wc(self):
        try:
            return self.json['wc']
        except KeyError:
            return 0.0

    def get_sort_method(self):
        try:
            return self.json['sort_method']
        except KeyError:
            return 0

    def get_notes(self):
        try:
            return self.json['notes']
        except KeyError:
            return ''

    def validate_guid(self, guid):
        user = self.db.users.find_one({'user_guid':guid})
        if user is None:
            raise InvalidUserError()

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

    def handle_request(self):
        try:
            self.json_in_request()
            self.check_required_properties()
            self.validate_guid(self.json['userGuid'])
            base = Base.Base(
                text=self.get_text(),
                cosine=self.get_cosine(),
                weight=self.get_weight(),
                format=self.get_format(),
                domain=self.get_domain(),
                space=self.get_space(),
                sort_method=self.get_sort_method(),
                wc = self.get_wc(),
                notes = self.get_notes()
            )
            self.write(base.query())
        except JSONMissingError:
            self.write(tornado.escape.json_encode({'error':'no JSON found'}))
        except JSONPropertyMissingError, e:
            self.write(tornado.escape.json_encode({'error':e.message}))
        except InvalidUserError:
            self.write(tornado.escape.json_encode({'error':'invalid user guid'}))
