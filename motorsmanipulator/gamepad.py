import pygame
from PyQt4.QtCore import QThread, pyqtSignal
from servers import clienttcp

class joystickThread(QThread):

    buttonPushed = pyqtSignal(int)
    buttonReleased = pyqtSignal(int)
    axisMoved = pyqtSignal(int, float)

    def __init__(self, parent=None):
        super(joystickThread, self).__init__(parent)
        self.EVENTS = {
            pygame.JOYBUTTONUP : lambda event: self.buttonPushedHandler(event),
            pygame.JOYAXISMOTION : lambda event: self.axisMovedHandler(event),
        }
        self.axisDict={}
        self.axisMovedCounter = 0
        self.axisFun = None
        self.buttonsFun = None
        self.my_joystick = None
        self.stop = False

    def init(self, joystickNum):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > joystickNum:
            self.my_joystick = pygame.joystick.Joystick(joystickNum)
            self.my_joystick.init()
        else:
            raise Exception("Joystick not connected")

    def finish(self):
        self.my_joystick = None
        self.terminate()

    def run(self):
        print "running"
        if self.my_joystick is not None and not self.stop:
            while True:
                self.g_keys = pygame.event.get()
                for event in self.g_keys:
                    if event.type in self.EVENTS:
                        self.EVENTS[event.type](event)
        else:
            raise Exception("Joystick not connected")


    def axisMovedHandler(self, event):
        if self.axisMovedCounter==0:
            if not self.axisFun is None:
                self.axisFun(event.axis, event.value)
            """if event.axis in self.axisDict:
                frame = "(" + str(self.axisDict[event.axis]) + ",S," + str(event.value) + ")"
                response = clienttcp.tcpConnection("localhost", 9998, frame)
                if response is not None:
                    self.axisMoved.emit(event.axis, event.value)"""
            self.axisMovedCounter = 10
        else:
            self.axisMovedCounter-=1

    def buttonPushedHandler(self, event):
        if not self.buttonsFun is None:
            self.buttonsFun(event.button)
