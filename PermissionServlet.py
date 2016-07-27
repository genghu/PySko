import tornado.web
import tornado.escape

import pymongo

from PermissionManager import PermissionManager

class PermissionServlet(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy
        self.pm = PermissionManager()

    @tornado.web.authenticated
    def get(self):
        self.handle_request()
    
    @tornado.web.authenticated
    def post(self):
        self.handle_request()

    def handle_request(self):
        currentNickname = ''
        currentUser = self.current_user
        if currentUser is None:
            self.write(tornado.escape.json_encode({
                'error': 'Not logged in'
            }))
            return
        currentNickname = currentUser['email']

        # get json
        json = self.get_argument("json", None)
        json_decoded = tornado.escape.json_decode(json);
        guid = json_decoded['guid']
        perm = json_decoded['permission']
        nickname = json_decoded['nickname']
        m = json_decoded['method']
        source = json_decoded['source']
        try:
            sendEmail = json_decoded['sendEmail']
        except KeyError:
            pass
        
        if m == 'search':
            searchTerm = json_decoded['searchTerm']

        permission = self.getIntPerm(perm)
        method = self.getIntMethod(m)
        permissionExist = self.pm.checkPermission(nickname, guid, permission)
        isOwner = self.pm.checkPermission(nickname, guid, 8)
        isCreator = self.pm.checkPermission(nickname, guid, 4)
        isCollaborator = self.pm.checkPermission(nickname, guid, 2)
        isViewer = self.pm.checkPermission(nickname, guid, 1)

        level = self.pm.getPermissionLevel(currentNickname, guid)

        if method == 0:
            pass
        elif method == 1:
            pass
        elif method == 2:
            if permissionExist == True:
                self.write(tornado.escape.json_encode({
                    'permissionExists': True
                }))
            else:
                self.write(tornado.escape.json_encode({
                    'permissionExists': False
                }))
            return
        elif method == 3:
            if level < 2:
                self.write(tornado.escape.json_encode({
                    'error':'Must be owner to access permissions'
                }))
            else:
                self.write(tornado.escape.json_encode({
                    'permissionLevel': self.pm.getPermissionLevel(nickname, guid)
                }))
        elif method == 4:
            pass
        


    def getIntPerm(self, p):
        p = p.lower()

        if p == 'creator':
            return 8
        elif p == 'owner':
            return 4
        elif p == 'collaborator':
            return 2
        elif p == 'viewer':
            return 1
        else:
            return -1

    def getIntMethod(self, m):
        m = m.lower()

        if m == 'grant':
            return 0
        elif m == 'revoke':
            return 1
        elif m == 'check':
            return 2
        elif m == 'get':
            return 3
        elif m == 'search':
            return 4
        else:
            return -1

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return None
        return tornado.escape.json_decode(user)
