import tornado.web
import tornado.escape

from SKOLogService import SKOLogService

import urllib
import json

class SKOLogServiceWrapper(tornado.web.RequestHandler):
    def initialize(self):
        self.skoLogService = None

    @tornado.web.authenticated
    def get(self):
        self.handleRequest()

    @tornado.web.authenticated
    def post(self):
        self.handleRequest()

    def handleRequest(self):


        json_str = self.get_argument("json",None)
        if json_str==None:

            action = self.get_argument("action", None)
            guid = self.get_argument("guid", None)
            log = self.get_argument("log", None)
            sid = self.get_argument("SID", None)
            srt = self.get_argument("SRT", None)
        else:
            json_obj = json.loads(json_str)
            if "action" in json_obj:
                action = json_obj["action"]
            else:
                action = None

            if "guid" in json_obj:
                guid = json_obj["guid"]
            else:
                guid = None
            if "SID" in json_obj:
                sid = json_obj["SID"]
                if sid=="":
                    sid=None
            else:
                sid = None
            if "SRT" in json_obj:
                srt = json_obj["SRT"]
                if srt=="":
                    srt=None
            else:
                srt = None
            if "log" in json_obj:
                log = json_obj["log"]
            else:
                log = None

        user = self.current_user["email"]


        self.skoLogService = SKOLogService(action, guid, log, user,sid,srt)
        results = self.skoLogService.go()

        if action == "create":
            self.write(results)
        else:
            self.write(urllib.unquote((str(results)).decode('unicode_escape')))
            # self.render('skoLogs.html', 
            #     logs = list(results)
            # )


    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return None
        return tornado.escape.json_decode(user)