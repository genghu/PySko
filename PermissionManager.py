import pymongo

class PermissionManager:
    def __init__(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy
#        self.logfile = open('C:/atl.log', 'a')

    def checkPermission(self, nickname, guid, permission):
        if not self.permissionExists(nickname, guid):
            return False
        else:
            p = self.db.permissions.find_one({
                'nickname': nickname,
                'guid': guid
            })
 #           print >> self.logfile, 'hello world'
 #           print >> self.logfile, 'actual: %d, requested: %d' % (p['permission'], permission)
            if p['permission'] >= permission:
                return True
            return False

    def permissionExists(self, nickname, guid):
        exists = self.db.permissions.find_one({
            'nickname': nickname,
            'guid': guid
        })
#        print >> self.logfile, exists
        if exists is None:
#            print >> self.logfile, 'nope'
            return False
#        print >> self.logfile, 'yeah'
        return True

    def getPermission(self, nickname, guid):
        p = self.db.permissions.find_one({
            'nickname': nickname,
            'guid': guid
        })
        return p

    def getPermissionLevel(self, nickname, guid):
        if not self.permissionExists(nickname, guid):
            return 0
        p = self.getPermission(nickname, guid)
        return p['permission']
