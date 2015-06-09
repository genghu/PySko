import tornado.web

import urllib

import pymongo

import json
import datetime

from ATLiteExceptions import *



class RetrieveBookmarks(tornado.web.RequestHandler):
	def initialize(self):
		self.connection = pymongo.connection.Connection()
		self.db = self.connection.atlitepy

	def get(self):
		json_str = self.get_argument('json', None)
		if json_str==None:
			guid = self.get_argument('guid', None)
			email = self.get_argument('user', None)
		else:
			json_obj = json.loads(json_str)
			if "guid" in json_obj:
				guid = json_obj["guid"]
			else:
				guid = None			
		
			if "user" in json_obj:
				email = json_obj["user"]
			else:
				user = self.get_current_user()
				email = user["email"]
				print email
			
			if "x" in json_obj:
				try:
					numOfBookmarks = int(json_obj["x"])
				except:
					numOfBookmarks = 20
			else:
				numOfBookmarks = 20				

		bookmarks = list(self.db.bookmarks.find({"email":email, "guid":guid}).sort('time', pymongo.DESCENDING).limit(numOfBookmarks))
		print bookmarks
		json_obj = {}
		i=1;
		for bk in bookmarks:
			bmark = {}
			bmark['email']=bk['email']
			bmark['guid'] = bk['guid']
			bmark['notes'] = bk['notes']
			bmark['bookmark']=bk['bookmark']
			bmark['datetime']=bk['time'].strftime("%A, %B %d, %Y %H:%M:%S")
			#json_obj.append(bmark)
			key='bkm'+str(i)
			json_obj[key]=bmark
			i=i+1

		self.write( urllib.unquote(json.dumps(json_obj)))

	def get_current_user(self):
		user = self.get_secure_cookie("user")
		if not user:
			return None
		return tornado.escape.json_decode(user)