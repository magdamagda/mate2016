import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import manipulatorGUI
import gamepad
import time
from servers import clienttcp

AXES_DICT = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5"
}

class Manipulator(manipulatorGUI.ManipulatorGUI):
    def __init__(self, parent=None, joystickNum=0, host = "localhost", port = 9998):
        super(Manipulator, self).__init__(parent)
        self.gamepad = None
        self.joystickNum=joystickNum
        self.host = host
        self.port = port
        #self.sender = tcpSender(self)
        self.btnStart.clicked.connect(self.start)
        #self.sender.answerRecived.connect(self.moveAxes)

    def start(self):
        self.initGamepad(self.joystickNum)
        if self.gamepad is not None:
            self.gamepad.axisMoved.connect(self.moveAxes)
            self.gamepad.start()

    def initGamepad(self, joystickNum):
        try:
            self.gamepad = gamepad.joystickThread(None, joystickNum)
            self.log.append("Joystick connected")
        except Exception as e:
            print str(e)
            self.log.append(str(e))

    def moveAxes(self, axe, value):
        self.log.append(AXES_DICT[axe] + "  " + str(value))

    def responseAnalyze(self, respose):
        self.log.append("confirmed")

class tcpSender(QObject):

    answerRecived = pyqtSignal(int, float)

    def __init__(self, parent=None):
        super(tcpSender, self).__init__(parent)

    def sendRequest(self, axe, value):
        frame = "(A" + AXES_DICT[axe] + ",S," + str(value) + ")"
        response = clienttcp.tcpConnection(self.parent().host, self.parent().port, frame)
        if response is not None:
            self.answerRecived.emit(axe, value)

app = QApplication(sys.argv)
buttons = Manipulator()
buttons.show()
app.exec_()