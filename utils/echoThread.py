from PyQt4.QtCore import *
import time
import frames

class echoThread(QThread):

    connectionState = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self, parent=None, host = "localhost", port = 9998):
        super(echoThread, self).__init__(parent)
        self.refresh = 10
        self.host = host
        self.port = port
        self.connected = False

    def run(self):
        print "running"
        while not self.connected:
            print "echo thread"
            try:
                self.connected = frames.echo(self.host, self.port)
                self.connectionState.emit(self.connected)
            except Exception as e:
                self.error.emit(str(e))
            time.sleep(self.refresh)

    def setRefresh(self, value):
        print "set refresh"
        print value
        self.refresh = value