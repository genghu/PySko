import tornado.web
import tornado.escape
import tornado.httpclient

import pymongo

import uuid
import urllib

class AddPermissions(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy
#        self.logfile = open('c:/atl.log', 'a')

    @tornado.web.asynchronous
    def post(self):
#        print >> self.logfile, 'addPermissions'
        userGuid = self.get_argument('userGuid', None)
        emails = self.get_argument('emails', None)
        permissionLevel = self.get_argument('permissionLevel', None)
        skoGuid = self.get_argument('skoGuid', None)
        sendEmail = self.get_argument('sendEmail', False)

        if sendEmail == 'true':
            sendEmail = True
        else:
            sendEmail = False

        added = []

        # TODO: validate user permissions
        for email in emails.split(' '):
#            print >> self.logfile, "looking up user: '%s'" % email
            p = {}
            p['guid'] = skoGuid
            p['permission'] = int(permissionLevel)
            p['inTrash'] = 0

            user = self.db.users.find_one({'email': email})
            if user is not None:
                p['nickname'] = user['email']
            else:
                userGuid = str(uuid.uuid4())
                u = {}
                u['user_guid'] = userGuid
                u['email'] = email
                self.db.users.insert(u)

                p['nickname'] = u['email']

            permission_exists = self.db.permissions.find_one(p)
            if permission_exists is None:
                self.db.permissions.insert(p)
                added.append(email)

            data = tornado.escape.json_encode({'success':added})

            if len(added) > 0 and sendEmail == True:
 #               print >> self.logfile, 'send email'
                self.write(data)
                self.send_email(added, userGuid, int(permissionLevel))
            else:
 #               print >> self.logfile, len(added)
 #               print >> self.logfile, sendEmail
 #               print >> self.logfile, 'don\'t send email'
                self.write(data)
                self.finish()

    def send_email(self, added, userGuid, level):
#        print >> self.logfile, 'sending email'
        http = tornado.httpclient.AsyncHTTPClient()
        json = {}
        json['userGuid'] = userGuid
        json['to_addrs'] = ','.join(added)
        json['subject'] = "You've been invited to a SKO"
        json['message'] = "You have been granted permission level: %d" % (level)
        
        request = tornado.httpclient.HTTPRequest(
            url='http://localhost:8888/emailer',
            method='POST',
            body=urllib.urlencode({"json":tornado.escape.json_encode(json)})
        )
        http.fetch(request, callback=self.on_response)
        self.finish()

    def on_response(self, response):
        pass
