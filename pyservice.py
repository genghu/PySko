import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

import ATLServer

class AppServerSvc(win32serviceutil.ServiceFramework):
	_svc_name_ = "ATLiteServer"
	_svc_display_name_ = "ATLite Server"

	def __init(self, args):
		win32serviceutl.ServiceFramework.__init__(self, args)
		self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
		socket.setdefaulttimeout(60)

	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		exit(0)

	def SvcDoRun(self):
		servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
							  servicemanager.PYS_SERVICE_STARTED,
							  (self._svc_name_,''))
		self.main()

	def main(self):
		atlserver = ATLServer.ATLServer()
		atlserver.run()

if __name__ == '__main__':
	win32serviceutil.HandleCommandLine(AppServerSvc)