from PyQt4.QtCore import *
import time
import socket

from queue import queue

class commThread(QThread):

    frameRecived = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, q = queue(), host = "localhost", port = 9998, delay = 0.2):
        super(commThread, self).__init__()
        self.delay = delay
        self.host = host
        self.port = port
        self.q = q
        self.stop = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)
        self.sock.connect((host, port))
        self.counter = 0

    def run(self):
        print "comm running"
        while(not self.stop):
            try:
                if not self.q.isEmpty():
                    frame = self.q.pop()
                    print frame
                    self.sock.sendall(frame)
                    self.counter += 1
                    received = self.sock.recv(1024)
                    self.frameRecived.emit(format(received))
            except Exception as e:
                self.error.emit(str(e))
            time.sleep(self.delay)
        self.sock.close()

    def stop(self):
        self.stop = True