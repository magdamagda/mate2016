from PyQt4.QtCore import *
import time
import clienttcp

class tcpThread(QThread):

    paramsRetrived = pyqtSignal(dict)

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
            params = self.getAllParams()
            self.paramsRetrived.emit(params)
            time.sleep(self.refresh)

    def getAllParams(self):
        frames = ""
        for p in self.params:
            frames += "(" + p + ",G)"
        print frames
        response = clienttcp.tcpConnection(self.host, self.port, frames)
        if response is not None:
            return self.parseResponse(response)
        return {}

    def setRefresh(self, value):
        print "set refresh"
        print value
        self.refresh = value

    def parseResponse(self, response):
        result = {}
        frames = response.split("(")
        for frame in frames:
            frame = frame[0:-1]
            splitted = frame.split(",")
            if len(splitted) > 2:
                result[splitted[0]] = int(splitted[2])
        return result