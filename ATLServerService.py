import os
import time
import traceback
import win32service
import win32serviceutil
import win32api
import win32con
import tornado.web
import tornado.ioloop
from ATLiteApplication import ATLiteApplication

ERRFILE = "c:/err.txt"

class ATLServerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "atlserver_multi_lang_production"
    _svc_display_name_ = "ATL Server Multi Lang Production"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.isAlive = True

    def SvcDoRun(self):
        import servicemanager
        try:
            atliteapplication = ATLiteApplication()
            atliteapplication.listen(8889)
            tornado.ioloop.IOLoop.instance().start()
        except:
            time_s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            errfile = open(ERRFILE, "w")
            errfile.write(time_s + "\n")
            traceback.print_exc(file=errfile)
            errfile.close()

    def SvcStop(self):
        import servicemanager

        servicemanager.LogInfoMsg("atlserver - Recieved stop signal")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.isAlive = False

def ctrlHandler(ctrlType):
    return True

if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)
    win32serviceutil.HandleCommandLine(ATLServerService)
