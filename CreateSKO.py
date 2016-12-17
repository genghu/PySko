import tornado.web
import tornado.escape
import tornado.httpclient 

import uuid
import datetime
import urllib

import pymongo

from ATLiteExceptions import *

from PermissionManager import PermissionManager

class CreateSKO(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy
        self.mostRecentGuid = ''
        self.pm = PermissionManager()

    @tornado.web.authenticated
    def get(self):
        self.handle_request()

    @tornado.web.authenticated
    def post(self):
        self.handle_request()

    def handle_request(self):
        json = self.get_argument('json', None)
	self.message = 'no message'
        jsonObject = tornado.escape.json_decode(json)
        currentUser = self.current_user
        if currentUser is None:
            self.write(tornado.escape.json_encode({
                'loginUrl': '/realLogin'
            }))
            return
        try:
            hasGuid = jsonObject['guid']
            self.updateScript(jsonObject)
            self.write(tornado.escape.json_encode({
                'guid': self.mostRecentGuid,
		'message': self.message
            }))
        except KeyError:
            self.createScript(jsonObject)
            self.write(tornado.escape.json_encode({
                'guid': self.mostRecentGuid,
		'message': self.message
            }))
        except OtherError:
            self.write(tornado.escape.json_encode({
                'error': 'Must be collaborator to edit script'
            }))

    def updateScript(self, jsonObject):
        guid =  jsonObject['guid']
        scriptObject = self.getSKOScriptByGUID(guid)
	if scriptObject is None:
	    self.createWithGUID(jsonObject)
	else:
	    
            if not self.pm.checkPermission(self.current_user['email'], guid, 2):
                raise OtherError()
            scriptObject['componentType'] = jsonObject['componentType']
            scriptObject['notes'] = jsonObject['notes']
            scriptObject['published'] = jsonObject['published']
            scriptObject['resourceLocation'] = jsonObject['resourceLocation']
            scriptObject['resourceType'] = jsonObject['resourceType']
            scriptObject['scriptContent'] = jsonObject['scriptContent']
            scriptObject['scriptType'] = jsonObject['scriptType']
            scriptObject['timestamp'] = datetime.datetime.now()
            scriptObject['title'] = jsonObject['title']

            self.addScriptHistory(scriptObject)

            #scriptObject['scriptContent'] = None

            self.mostRecentGuid = guid

            self.db.skos.update({'guid': guid}, scriptObject)
   

	    # do update in the backup as well
            # the last parameter is 1, which means this is from update request 
	    # default is 0, no update
            self.doBackup(scriptObject,1)
 
    def createWithGUID(self, jsonObject):
        guid =  jsonObject['guid']
	scriptObject = {}
	#if not self.pm.checkPermission(self.current_user['email'], guid, 2):
	#    raise OtherError()
	scriptObject['guid'] = guid
	scriptObject['componentType'] = jsonObject['componentType']
	scriptObject['notes'] = jsonObject['notes']
	scriptObject['published'] = jsonObject['published']
	scriptObject['resourceLocation'] = jsonObject['resourceLocation']
	scriptObject['resourceType'] = jsonObject['resourceType']
	scriptObject['scriptContent'] = jsonObject['scriptContent']
	scriptObject['scriptType'] = jsonObject['scriptType']
	scriptObject['timestamp'] = datetime.datetime.now()
	scriptObject['title'] = jsonObject['title']
	scriptObject['createdBy'] = self.current_user['email']

	self.addScriptHistory(scriptObject)

	scriptObject['scriptContent'] = None

	self.mostRecentGuid = guid
	self.message = 'created with existing guid: %s' % (guid)
	self.db.skos.insert(scriptObject)

	if jsonObject['source'].lower() == 'authoringtool':
    	    self.db.permissions.update({
        	'nickname': scriptObject['createdBy'],
        	'guid': scriptObject['guid'],
        	'permission': 8
    	    }, {
        	'nickname': scriptObject['createdBy'],
        	'guid': scriptObject['guid'],
        	'permission': 8,
            'inTrash':0
            }, upsert=True)    

    def createScript(self, jsonObject):
        scriptObject = self.jsonObjectToSKOScript(jsonObject)
        self.addScriptHistory(scriptObject)

        #scriptObject['scriptContent'] = None
        if jsonObject['source'].lower() == 'authoringtool':
            self.db.permissions.update({
                'nickname': scriptObject['createdBy'],
                'guid': scriptObject['guid'],
                'permission': 8
            }, {
                'nickname': scriptObject['createdBy'],
                'guid': scriptObject['guid'],
                'permission': 8,
                'inTrash':0
            }, upsert=True)
        self.db.skos.insert(scriptObject)

	# do the backup now 
        self.doBackup(scriptObject)

    def doBackup(self, scriptObject,update=0): 
	#now save a copy as backup, guid and lastUpdatedBy hardcoded 
        http_client = tornado.httpclient.HTTPClient()
        #scriptObject['guid'] = '6a78c27d-73e3-4e08-bc2f-a0ff39fd7dc1'
        scriptObject['title'] += '- Created by '+scriptObject['createdBy'] 
        scriptObject['createdBy'] = 'xiangenhu@gmail.com'
        scriptObject['lastUpdatedBy'] = 'xiangenhu@gmail.com'
        scriptObject['backupreq'] = 1
        scriptObject['update'] = update
        scriptObject['source'] = 'authoringtool'

        nso = scriptObject
        nso['timestamp']= str(nso['timestamp'])
        nso['_id']= str(nso['_id'])
        #print '>>>>>>',nso
        body=urllib.urlencode({"json":tornado.escape.json_encode(nso)})
        #body=urllib.urlencode({"json":scriptObject})
        #print '>>>>>>>>>',body
	try:
		#headers = {'Content-Type': 'application/json; charset=UTF-8'}
		headers = None  
		req = tornado.httpclient.HTTPRequest("http://backup.skoonline.org/create",method="POST",body=body,headers=headers)
    		response = http_client.fetch(req)
    		print response.body
	except tornado.httpclient.HTTPError as e:
    		print("Error: " + str(e))
	except Exception as e:
    		print("Error: " + str(e))

    def addScriptHistory(self, scriptObject):
        history = {}
        history['guid'] = scriptObject['guid']
        history['scriptContent'] = scriptObject['scriptContent']
        history['timestamp'] = datetime.datetime.now()
        history['title'] = scriptObject['title']
        history['notes'] = scriptObject['notes']
        history['historyGuid'] = str(uuid.uuid4())
        if self.current_user is None:
            history['lastUpdatedBy'] = scriptObject['createdBy']
        else:
            history['lastUpdatedBy'] = self.current_user['email']

        self.db.history.insert(history)

    def jsonObjectToSKOScript(self, jsonObject):
        scriptObject = {}
        scriptObject['componentType'] = jsonObject['componentType']
        scriptObject['createdBy'] = self.current_user['email']
        _uuid = str(uuid.uuid4())
        self.mostRecentGuid = _uuid
        scriptObject['guid'] = _uuid
        scriptObject['notes'] = jsonObject['notes']
        scriptObject['published'] = jsonObject['published']
        scriptObject['resourceLocation'] = jsonObject['resourceLocation']
        scriptObject['resourceType'] = jsonObject['resourceType']
        scriptObject['scriptContent'] = jsonObject['scriptContent']
        scriptObject['scriptType'] = jsonObject['scriptType']
        scriptObject['timestamp'] = datetime.datetime.now()
        scriptObject['title'] = jsonObject['title']

        return scriptObject

    def getSKOScriptByGUID(self, guid):
        scripts = self.db.skos.find({'guid': guid})
        if scripts.count() > 0:
            return scripts[0]
	return None


    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return None
        return tornado.escape.json_decode(user)
