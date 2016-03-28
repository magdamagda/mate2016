from PyQt4.QtCore import *
import time
import clienttcp

class tcpThreadSingle(QThread):

    responseRecived = pyqtSignal(str)

    def __init__(self, frames, host = "localhost", port = 9998):
        super(tcpThreadSingle, self).__init__()
        self.host = host
        self.port = port
        self.frames = frames

    def run(self):
        response = clienttcp.tcpConnection(self.host, self.port, self.frames)
        if response is not None:
            self.responseRecived.emit(response)
