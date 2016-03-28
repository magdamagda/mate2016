from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from servers import tcpThread
from motorsGUI import MotorsGUI
import gamepad
from servers import clienttcp


paramsDict = ["M1", "M2", "M3", "M4", "M5", "M6", "AX", "AY", "AZ"]
AXIS_MOTORS = {
    1: "M5",  #  left engine
    4: "M6",  #  right engine
}

BUTTONS_MOTORS = {
    4: [("M1", 10), ("M2", 10), ("M3", 10), ("M4", 10)],  #  up
    5: [("M1", -10), ("M2", -10), ("M3", -10), ("M4", -10)],  #  down
    11: [("M1", -10), ("M2", -10), ("M3", 10), ("M4", 10)],  #  tilt forward
    12: [("M1", 10), ("M2", 10), ("M3", -10), ("M4", -10)],  # tilt backward
    13: [("M1", -10), ("M2", 10), ("M3", -10), ("M4", 10)],  # tilt left
    14: [("M1", 10), ("M2", -10), ("M3", 10), ("M4", -10)],  #  tilt right
}

class MainWindow(MotorsGUI):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.startBtn.clicked.connect(self.start)
        self.bgThread = tcpThread.tcpThread(self, paramsDict, "localhost", 9998)
        self.bgThread.paramsRetrived.connect(self.updateValues)
        self.bgThread.start()

        self.gamepad = gamepad.joystickThread()
        self.gamepad.axisMoved.connect(self.showMotorsValue)
        self.gamepad.axisDict=AXIS_MOTORS
        self.gamepad.axisFun = self.motorsControl
        self.gamepad.buttonsFun = self.topMotorsControl

    def start(self):
        if self.gamepad.isRunning():
            self.gamepad.finish()
            self.startBtn.setText("Start")
        else:
            self.initGamepad(int(self.inputPadNum.text()))
            if self.gamepad.isRunning():
                self.startBtn.setText("Stop")

    def initGamepad(self, joystickNum):
        try:
            self.gamepad.init(joystickNum)
            self.log.append("Joystick connected")
            self.gamepad.start()
        except Exception as e:
            print str(e)
            self.log.append(str(e))

    def updateValues(self, params):
        for param in  params:
            labelValue = getattr(self, "labelValue" + param)
            labelValue.setText(str(params[param]))

    def showMotorsValue(self, axe, value):
        self.log.append(str(axe) + "  " + str(value))

    def motorsControl(self, axis, value):
        if axis in AXIS_MOTORS:
            frame = "(" + str(AXIS_MOTORS[axis]) + ",S," + str(value*100) + ")"
            response = clienttcp.tcpConnection("localhost", 9998, frame)
            if response is not None:
                 self.showMotorsValue(axis, value*100)

    def topMotorsControl(self, button):
        if button in BUTTONS_MOTORS:
            frame = ""
            for item in BUTTONS_MOTORS[button]:
                frame += "(" + item[0] + ",S," + str(item[1]) + ")"
            response = clienttcp.tcpConnection("localhost", 9998, frame)
            if response is not None:
                 self.log.append(frame)



app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
app.exec_()