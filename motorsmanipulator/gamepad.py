import pygame
from PyQt4.QtCore import QThread, pyqtSignal

class joystickThread(QThread):

    buttonPushed = pyqtSignal(int)
    buttonReleased = pyqtSignal(int)
    axisMoved = pyqtSignal(int, float)

    def __init__(self, parent=None, joystickNum=0):
        super(joystickThread, self).__init__(parent)
        pygame.init()
        pygame.joystick.init()
        self.my_joystick = None
        if pygame.joystick.get_count() > joystickNum:
            self.my_joystick = pygame.joystick.Joystick(joystickNum)
            self.my_joystick.init()
        else:
            raise Exception("Joystick not connected")
        self.EVENTS = {
            pygame.JOYBUTTONUP : lambda event: self.buttonPushed.emit(event.button),
            pygame.JOYBUTTONDOWN : lambda event: self.buttonReleased.emit(event.button),
            pygame.JOYAXISMOTION : lambda event: self.axisMoved.emit(event.axis, event.pos),
        }

    def run(self):
        print "running"
        if self.my_joystick is not None:
            while True:
                self.g_keys = pygame.event.get()
                for event in self.g_keys:
                    if event.type in self.EVENTS:
                        self.EVENTS[event.type](event)
        else:
            raise Exception("Joystick not connected")

