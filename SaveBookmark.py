import tornado.web

import urllib

import pymongo

from pymongo import MongoClient

import json
import datetime

from ATLiteExceptions import *
from gmail import GMailPy



class SaveBookmark(tornado.web.RequestHandler):
	def initialize(self):
		#self.connection = pymongo.connection.Connection()
		#self.db = self.connection.atlitepy
		self.client = MongoClient()
		self.db = client.atlitepy

	def get(self):
		json_str = self.get_argument('json', None)
		if json_str==None:
			guid = self.get_argument('guid', None)
			bookmark = self.get_argument('bookmark', None)
			notes = self.get_argument('notes', None)
			email = self.get_argument('user', None)
		else:
			json_obj = json.loads(json_str)

			if "guid" in json_obj:
				guid = json_obj["guid"]
			else:
				guid = None

			if "bookmark" in json_obj:
				bookmark = json_obj["bookmark"]
			else:
				bookmark = None

			if "notes" in json_obj:
				notes = json_obj["notes"]
			else:
				notes = None

			if "user" in json_obj:
				email = json_obj["user"]
			else:
				user = self.get_current_user()
				email = user["email"]
				print email

		self.db.bookmarks.insert( { "guid": guid, "email":email, "bookmark": bookmark, "notes": notes,  "time": datetime.datetime.now() } )		
		#self.send_email();
   
	def send_email(self):
		g = GMailPy()
		g.add_to_addr("iFaisalRahman@gmail.com")
		g.set_subject("TEST SUBJECT")
		g.set_message("TEST MSG")
		g.send_message()
	def get_current_user(self):
		user = self.get_secure_cookie("user")
		if not user:
			return None
		return tornado.escape.json_decode(user)     
