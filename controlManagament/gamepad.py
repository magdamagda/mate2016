import pygame
import time
from PyQt4.QtCore import QThread, pyqtSignal

PAD_INTERVAL = 0.2

class joystickThread(QThread):

    newState = pyqtSignal(dict, dict)

    def __init__(self, parent=None):
        super(joystickThread, self).__init__(parent)
        self.buttonsState = {}
        self.axesState = {}
        self.changedState = False
        self.my_joystick = None
        self.stop = False

    def init(self, joystickNum):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > joystickNum:
            self.my_joystick = pygame.joystick.Joystick(joystickNum)
            self.my_joystick.init()
            self.stop = False
        else:
            raise Exception("Joystick not connected")

    def finish(self):
        self.stop = True
        self.my_joystick = None

    def run(self):
        print "running"
        if self.my_joystick is not None:
            while not self.stop:
                self.g_keys = pygame.event.get()
                self.changedState = False
                self.readButtonsState()
                self.readAxesState()
                if self.changedState:
                    self.newState.emit(self.buttonsState, self.axesState)
                time.sleep(PAD_INTERVAL)

                """self.g_keys = pygame.event.get()
                for event in self.g_keys:
                    if event.type in self.EVENTS:
                        self.EVENTS[event.type](event)"""
        else:
            raise Exception("Joystick not connected")

    def setButtons(self, list):
        for item in list:
            self.buttonsState[item] = 0

    def setAxes(self, list):
        for item in list:
            self.axesState[item] = 0

    def readButtonsState(self):
        for btn in self.buttonsState:
            state = self.my_joystick.get_button(btn)
            if state!=self.buttonsState[btn]:
                self.buttonsState[btn] = state
                self.changedState = True

    def readAxesState(self):
        for ax in self.axesState:
            state = self.my_joystick.get_axis(ax)
            if state < 0.2 and state > -0.2:
                state = 0
            if state!=self.axesState[ax]:
                self.axesState[ax] = state
                self.changedState = True

