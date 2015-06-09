import tornado.web

import urllib

import pymongo

import re
import json

from ATLiteExceptions import *


class AdminScripts(tornado.web.RequestHandler):
    def initialize(self):
		'''self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy'''
    def get(self):

    	self.render('AdminScripts.html')

