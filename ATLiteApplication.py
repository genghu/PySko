import tornado.web

import os
import uuid
import base64

import pymongo
import pymongo.errors
from pymongo import MongoClient

import RootHandler
import LoginHandler
#import GIFTLoginHandler
import CreateSKO
import RetrieveSKO
import UpdateSKO
import ListSKOs
import SKOPermissions
import AddPermissions
import UpdatePermissions
import DeletePermissions
import SKOHistory
import ChangeDefaultHistory
import EMailer
import EmailTester
import RetrieveGUID
import ATLite
import CheckPermission
import BaseWrapper
import DomainList
import SpaceList
import SSAWrapper
import CompareText
import SSAAll
import SSASD
import LoginServlet
import RetrieveServlet
import PermissionServlet
import SKOLogServiceWrapper
import CrossDomainXMLHandler
import RetrieveAccountWrapper
import TrashSKO
import AdminScripts
import SKOAdmin
import DeleteSKOByAdmin
import SaveBookmark
import RetrieveBookmarks
#import MyScriptsServlet

import RedmineLoginHandler

global client

class ATLiteApplication(tornado.web.Application):
    def __init__(self):
        try:
            #self.connection = pymongo.connection.Connection()
	    client = MongoClient()
	    self.db = client.dsspp
        except pymongo.errors.AutoReconnect:
#            self.logfile = open('C:/atlapp.log', 'a')
#            print >> self.logfile, '*** atldsspp says: Error! Could not connect to MongoDB!'
#            self.logfile.close()
            exit()

        handlers = [
		#(r"/myscriptsdata", MyScriptsServlet.MyScriptsServlet),
            (r"/crossdomain.xml", CrossDomainXMLHandler.CrossDomain),
            (r"/", RootHandler.RootHandler),
            (r"/login", LoginServlet.LoginServlet),
            (r"/create", CreateSKO.CreateSKO),
            (r"/retrieve", RetrieveServlet.RetrieveServlet),
            (r"/update_sko", UpdateSKO.UpdateSKO),
            (r"/list_skos", ListSKOs.ListSKOs),
            (r"/permissions", SKOPermissions.SKOPermissions),
            (r"/addPermissions", AddPermissions.AddPermissions),
            (r"/updatePermissions", UpdatePermissions.UpdatePermissions),
            (r"/deletePermissions", DeletePermissions.DeletePermissions),
            (r"/history", SKOHistory.SKOHistory),
            (r"/changeDefaultHistory", ChangeDefaultHistory.ChangeDefaultHistory),
            (r"/emailer", EMailer.EMailer),
            (r"/email_tester", EmailTester.EmailTester),
            (r"/account", RetrieveGUID.RetrieveGuid),
            (r"/atlitepy", ATLite.ATLite),
            (r"/permission", PermissionServlet.PermissionServlet),
            (r"/permissions\.jsp.*", SKOPermissions.SKOPermissions),
            (r"/myScripts\.jsp", ListSKOs.ListSKOs),
            (r"/base", BaseWrapper.BaseWrapper),
            (r"/domainlist.xml", DomainList.DomainList),
            (r"/spaces.xml", SpaceList.SpaceList),
            (r"/ssa", SSAWrapper.SSAWrapper),
            (r"/comparetext", CompareText.CompareText),
            (r"/ssaall", SSAAll.SSAAll),
            (r"/ssasd", SSASD.SSASD),
            (r"/getaccount", RetrieveGUID.RetrieveGuid),
            (r"/googleLogin", LoginHandler.LoginHandler),
            (r"/realLogin", LoginHandler.LoginHandler),
            #(r"/realLogin", GIFTLoginHandler.LoginHandler),
            #(r"/redmineLogin", GIFTLoginHandler.LoginHandler),
            (r"/oauth2callback", LoginHandler.LoginHandler),
            (r"/skolog", SKOLogServiceWrapper.SKOLogServiceWrapper),
            (r"/retrieveRecord", SKOLogServiceWrapper.SKOLogServiceWrapper),
            (r"/profile", RetrieveAccountWrapper.RetrieveAccountWrapper),
            (r"/trashSKO", TrashSKO.TrashSKO),
            (r"/admindata", SKOAdmin.SKOAdmin),
            (r"/AdminScripts\.jsp.*", AdminScripts.AdminScripts),
            (r"/delete", DeleteSKOByAdmin.DeleteSKOByAdmin),
            (r"/savebookmark", SaveBookmark.SaveBookmark),
            (r"/retrievebookmark", RetrieveBookmarks.RetrieveBookmarks),
		
            (r"/redmineLogin2", RedmineLoginHandler.Main),
           # (r"/realLogin", RedmineLoginHandler.Main),
            (r"/redmineCallback", RedmineLoginHandler.Callback)


        ];

        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            login_url="/login",
            debug=True,
            google_oauth= dict(
                key='49505139072-gujig73jfg01famvd106cldnm1h9cgkl.apps.googleusercontent.com',
                secret='VEg5ou7ReKnZK-pomcOBDv9A'
            )
        )

        tornado.web.Application.__init__(self, handlers, **settings)
