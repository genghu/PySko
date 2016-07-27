import tornado.web

import urllib

import pymongo

import re
import json
import time

class SKOAdmin(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    def get(self):

        search_title = self.get_argument("title",None);
        search_type = self.get_argument("type",None);
        search_author = self.get_argument("author",None);
        search_date_start = self.get_argument("start_date",None);
        search_date_end = self.get_argument("end_date",None);
        #objectid = self.get_argument('objectid',None)
        if search_title==None:
            search_title=""
        if search_type==None:
            search_type=""
        if search_author==None:
            search_author=""
        if search_date_start==None:
            search_date_start=""            

        if search_date_end==None:
            search_date_end=""            

        skos = []
        sko_list = list(self.db.skos.find())
        script = {}
        for s in sko_list:
            script = {}
            script['title'] = (s['title']==None) if "" else s['title']
            if s['scriptType']==None:
                script['scriptType'] = ""
            else:
                script['scriptType'] = s['scriptType']

            script['guid']=(s['guid']==None) if "" else s['guid']
            script['lastUpdated']=s['timestamp'].strftime("%A, %B %d, %Y %H:%M:%S")
            script['published']=s['published']
            script['createdBy']=(s['createdBy']==None) if "" else s['createdBy']
            script['notes']=s['notes']
            if ( search_title.upper() in script['title'].upper() ) and( search_type.upper() in script['scriptType'] ) and (search_author.upper() in script['createdBy'].upper()) and (self.date_between (search_date_start,search_date_end,s['timestamp'].strftime("%m-%d-%Y"))):                
                skos.append(script)

        self.write( urllib.unquote(json.dumps(skos)))
        #return  json.dumps(skos)
    def date_between(self,start,end,sdate):
        sko_date = time.strptime(sdate, "%m-%d-%Y")
        if start==None or start=="" :
            sDate = time.strptime("01-31-2000", "%m-%d-%Y")
        else:
            sDate =  time.strptime(start, "%m/%d/%Y")

        if end==None or end=="":
            eDate = time.strptime("12-31-2050", "%m-%d-%Y")
        else:
            eDate =  time.strptime(end, "%m/%d/%Y")
        if sDate <= sko_date and eDate >= sko_date:
            return True
        else:
            return False




