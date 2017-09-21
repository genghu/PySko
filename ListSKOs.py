import tornado.web

import urllib

import pymongo
from pymongo import MongoClient

import re
import json

from ATLiteExceptions import *

class ListSKOs(tornado.web.RequestHandler):
    def initialize(self):
        #self.connection = pymongo.connection.Connection()
        #self.db = self.connection.atlitepy
	self.client = MongoClient()
	self.db = client.atlitepy

    @tornado.web.authenticated
    def get(self):
        try:
            creator = []
            owner = []
            collaborator = []
            viewer= []
            trash = []
            email = self.current_user['email']
            CBSLocation = '119.97.167.114/SKO2013/EditorPlayer'

            try:
                burl = self.get_argument('BURL')
            except:
                burl = CBSLocation
            
            # get rid of leading http:// 
            if 'http' in burl:
                burl = burl[7:]

            # get rid of trailing slash
            if burl[-1] == '/':
                burl = burl[:-1]

            
            try:
                burla = self.get_argument('BURLA')
            except:
                burla = "http://54.223.152.164:8099/1024768/generalv2/authoring.html";
            
            # get rid of leading http:// 
            if 'http' in burla:
                burla = burla[7:]

            # get rid of trailing slash
            if burla[-1] == '/':
                burla = burla[:-1]


            try:
                burlp = self.get_argument('BURLP')
            except:
                burlp = "http://54.223.152.164:8099/1024768/generalv2/ATL.html";
            
            # get rid of leading http:// 
            if 'http' in burlp:
                burlp = burlp[7:]

            # get rid of trailing slash
            if burlp[-1] == '/':
                burlp = burlp[:-1]

            try:
                development = self.get_argument('development')
            except:
                development = "None"   
            guid = self.db.users.find_one({'email':email})['user_guid']
            creator_skos_p = self.db.permissions.find({'nickname':email, 'permission': 8, 'inTrash':0})
            owner_skos_p = self.db.permissions.find({'nickname':email, 'permission': 4, 'inTrash':0})
            collaborator_skos_p = self.db.permissions.find({'nickname':email, 'permission': 2, 'inTrash':0})
            viewer_skos_p = self.db.permissions.find({'nickname':email, 'permission': 1, 'inTrash':0})
            trash_skos_p = self.db.permissions.find({'nickname':email, 'permission': 8, 'inTrash':1})
            for s in creator_skos_p:
                sko_guid = s['guid']
                sko = self.db.skos.find_one({'guid': sko_guid})
                most_recent_history = self.db.history.find({'guid': sko_guid}).sort('timestamp', pymongo.DESCENDING).limit(1)[0]
                s['skoTitle'] = self.unescape(most_recent_history['title'])  #urllib.unquote(most_recent_history['title'])
                s['creator'] = email
                s['updatedDate'] = most_recent_history['timestamp'].strftime("%A, %B %d, %Y %H:%M:%S")
                if sko == None:
                    s['scriptType'] = ""   
                else:
                    s['scriptType'] = sko['scriptType']#urllib.unquote(sko['scriptType'] )
                s['skoGuid'] = s['guid']
                s['CBSLocation'] = 'www.x-in-y.com'
                s['notes'] = urllib.unquote(most_recent_history['notes'])
                s['_id']=str(s["_id"]) #Change by Faisal
                creator.append(s)

            for s in owner_skos_p:
                sko_guid = s['guid']
                sko = self.db.skos.find_one({'guid': sko_guid})
                most_recent_history = self.db.history.find({'guid': sko_guid}).sort('timestamp', pymongo.DESCENDING).limit(1)[0]
                s['skoTitle'] = urllib.unquote(most_recent_history['title'])
                s['creator'] = email
                s['updatedDate'] = most_recent_history['timestamp'].strftime("%A, %B %d, %Y %H:%M:%S")
                if sko == None:
                    s['scriptType'] = ""   
                else:
                    s['scriptType'] = sko['scriptType']#urllib.unquote(sko['scriptType'])
                s['skoGuid'] = s['guid']
                s['CBSLocation'] = 'www.x-in-y.com'
                s['notes'] = urllib.unquote(most_recent_history['notes'])
                s['_id']=str(s["_id"])
                owner.append(s)

            for s in collaborator_skos_p:
                sko_guid = s['guid']
                sko = self.db.skos.find_one({'guid': sko_guid})
                most_recent_history = self.db.history.find({'guid': sko_guid}).sort('timestamp', pymongo.DESCENDING).limit(1)[0]
                s['skoTitle'] = urllib.unquote(most_recent_history['title'])
                s['creator'] = email
                s['updatedDate'] = most_recent_history['timestamp'].strftime("%A, %B %d, %Y %H:%M:%S")
                if sko == None:
                    s['scriptType'] = ""   
                else:
                    s['scriptType'] = sko['scriptType']#urllib.unquote(sko['scriptType'])
                s['skoGuid'] = s['guid']
                s['CBSLocation'] = 'www.x-in-y.com'
                s['notes'] = urllib.unquote(most_recent_history['notes'])
                s['_id']=str(s["_id"])
                collaborator.append(s)

            for s in viewer_skos_p:
                sko_guid = s['guid']
                sko = self.db.skos.find_one({'guid': sko_guid})
                most_recent_history = self.db.history.find({'guid': sko_guid}).sort('timestamp', pymongo.DESCENDING).limit(1)[0]
                s['skoTitle'] = urllib.unquote(most_recent_history['title'])
                s['creator'] = email
                s['updatedDate'] = most_recent_history['timestamp'].strftime("%A, %B %d, %Y %H:%M:%S") 
                if sko == None:
                    s['scriptType'] = ""   
                else:
                    s['scriptType'] = sko['scriptType']#urllib.unquote(sko['scriptType'])
                s['skoGuid'] = s['guid']
                s['CBSLocation'] = 'www.x-in-y.com'
                s['notes'] = urllib.unquote(most_recent_history['notes'])
                s['_id']=str(s["_id"])
                viewer.append(s)
   
            for s in trash_skos_p:
                sko_guid = s['guid']
                sko = self.db.skos.find_one({'guid': sko_guid})
                most_recent_history = self.db.history.find({'guid': sko_guid}).sort('timestamp', pymongo.DESCENDING).limit(1)[0]
                s['skoTitle'] = self.unescape(most_recent_history['title'])  #urllib.unquote(most_recent_history['title'])
                s['creator'] = email
                s['updatedDate'] = most_recent_history['timestamp'].strftime("%A, %B %d, %Y %H:%M:%S")
                if sko == None:
                    s['scriptType'] = ""   
                else:
                    s['scriptType'] = sko['scriptType']#urllib.unquote(sko['scriptType'] )
                s['skoGuid'] = s['guid']
                s['CBSLocation'] = 'www.x-in-y.com'
                s['notes'] = urllib.unquote(most_recent_history['notes'])
                s['_id']=str(s["_id"]) #Change by Faisal
                trash.append(s)        
 
                
            self.render('ListSKOs00New.html', 
                created = urllib.quote(json.dumps(creator)),#creator,#urllib.quote(json.dumps(creator)),#creator, #Change by Faisal
                owned = urllib.quote(json.dumps(owner)),
                collaborated = urllib.quote(json.dumps(collaborator)),
                viewable = urllib.quote(json.dumps(viewer)),
                trash = urllib.quote(json.dumps(trash)),
                creator_count = len(creator),
                owner_count = len(owner),
                collaborator_count = len(collaborator),
                viewer_count = len(viewer),
                email = email,
                CBSLocation = self.get_user_country(),
                burl = burl,
                burla = burla,
                burlp=burlp
            )            
        
        except UserNotLoggedInError:
            self.render('UserNotLoggedIn.html')

    def get_user_country(self):
        ip = self.request.remote_ip
        data = urllib.urlopen('http://api.wipmania.com/%s' % (ip))
        country = data.readlines()[0]
        if country == 'CN':
            return '119.97.167.4'
        return 'www.x-in-y.com'

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            self.redirect('/realLogin?nextUrl=myScripts.jsp')
            return None
        return tornado.escape.json_decode(user)

    def unescape(self, script):
        script = re.sub("%u(..)(..)",r"\u\1\2",script)
        return urllib.unquote(script.decode('unicode_escape'))#urllib.unquote(script)
