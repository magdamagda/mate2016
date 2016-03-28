from PyQt4.QtCore import *
import time
import clienttcp
import frames

class tcpThread(QThread):

    paramsRetrived = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, parent=None, paramsList = [], host = "localhost", port = 9998):
        super(tcpThread, self).__init__(parent)
        self.refresh = 5
        self.params = paramsList
        self.host = host
        self.port = port

    def run(self):
        print "running"
        while(1):
            print "get params"
            try:
                params = frames.getAllParams(self.params, self.host, self.port)
                print params
                self.paramsRetrived.emit(params)
            except Exception as e:
                self.error.emit(str(e))
            time.sleep(self.refresh)

    def setRefresh(self, value):
        print "set refresh"
        print value
        self.refresh = value