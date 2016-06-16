from PyQt4.QtCore import *
import time
import socket
import utils.frames

class tcpThread(QThread):

    paramsRetrived = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, parent=None, paramsList = [], host = "localhost", port = 9998):
        super(tcpThread, self).__init__(parent)
        self.refresh = 5
        self.params = paramsList
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        print "running"
        #self.sock.connect((self.host, self.port))
        while(1):
            print "get params"
            params=[]
            try:
                for p in self.params:
                    print p
                    print utils.frames.getParamFrame(p[0], p[1])
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.connect((self.host, self.port))
                    self.sock.sendall(utils.frames.getParamFrame(p[0], p[1]))
                    received = self.sock.recv(1024)
                    self.sock.close()
                    print received
                    name, number, data = utils.frames.parseParamResponseFrame(received)
                    params.append((name, number, data))
                self.paramsRetrived.emit(params)
            except Exception as e:
                print str(e)
                self.error.emit(str(e))
            time.sleep(self.refresh)
        #self.sock.close()

    def setRefresh(self, value):
        print "set refresh"
        print value
        self.refresh = value