import pymongo

import datetime
import json

class SKOLogService:
    def __init__(self, action, guid, log=None, user=None, sid=None, srt=None):
        self.action = action
        self.guid = guid
        self.log = log
        self.user = user
        self.sid  = sid
        self.srt   = srt
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    def go(self):
        if self.action == "create":
            return self.create()
        else:
            return self.view()

    def create(self):
        new_log = {
            "guid":self.guid,
            "user":self.user,
            "log":self.log,
            "SID":self.sid,
            "SRT":self.srt,
            "timestamp":datetime.datetime.now()
        }

        self.db.sko_logs.insert(new_log)

        return "new log created"

    def view(self):
        if self.sid!=None and self.srt!=None and self.guid!=None:
            query = {
            "guid":self.guid,
            "user":self.user,
            "SID":self.sid,
            "SRT":self.srt
            }
        else:
            if self.sid==None and self.srt!=None and self.guid!=None:
                query = {
                "guid":self.guid,
                "user":self.user,
                "SRT":self.srt
                }
            else:
                if self.sid!=None and self.srt==None and self.guid!=None:
                    query = {
                    "guid":self.guid,
                    "user":self.user,
                    "SID":self.sid
                    }
                else:
                    if self.sid==None and self.srt==None and self.guid!=None:
                        query = {
                        "guid":self.guid,
                        "user":self.user
                        }


        results = list(self.db.sko_logs.find(query).sort("timestamp", pymongo.DESCENDING).limit(1000))
        for result in results:
            result["_id"] = str(result["_id"])
            result["timestamp"] = str(result["timestamp"]) 
        return json.dumps(results)
        #return self.db.sko_logs.find_one({"user":"faisalbuet03@gmail.com"}) 
        #return  self.db.sko_logs.find(query).sort("timestamp", pymongo.DESCENDING).limit(1000)