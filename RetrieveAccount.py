import pymongo
from pymongo import MongoClient

import datetime
import urllib
from bson import ObjectId
import json

class RetrieveAccount:
    def __init__(self, action, name=None, preference=None, preferenceTitle=None, timestamp=None ,profileID=None,show_all=None):
        self.action = action
        self.name = name
        self.preference = preference
        self.preferenceTitle = preferenceTitle
        self.timestamp  = timestamp
        self.profileID   = profileID#"HELLO PROFILE"
        self.show_all = show_all
        #self.connection = pymongo.connection.Connection()
        #self.db = self.connection.atlitepy
	self.client = MongoClient()
	self.db = client.atlitepy

    def go(self):
        if self.action == "create":
            return self.create()
        else:
            if self.action == "update":
                return self.update()
            else:
                return self.view()

    def create(self):
        new_account = {
            "name":self.name,
            "preference":self.preference,
            "preferenceTitle":self.preferenceTitle,
            "timestamp":datetime.datetime.now()
        }

        self.db.sko_account.insert(new_account)

        return "new account created"

    def update(self):
        new_account = {
            "name":self.name,
            "preference":self.preference,
            "preferenceTitle":self.preferenceTitle,
            "timestamp":datetime.datetime.now()
        }
        print "_________UPDATE_________"
        _id = ObjectId(self.profileID)
        print _id
        self.db.sko_account.update({"_id":_id},new_account,True)
        return "Account Updated"

    def view(self):
        results = list(self.db.sko_account.find({"name":self.name}).sort("timestamp", pymongo.DESCENDING))
        
        for result in results:
            result["_id"] = str(result["_id"])
            result["timestamp"] = str(result["timestamp"])
        if len(results) == 0:
            return ('{"profile":"You have not create any profile"}')
        if self.show_all == "1":
            return json.dumps(results)
        else:
            return json.dumps(results[0])
