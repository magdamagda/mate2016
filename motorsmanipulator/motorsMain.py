from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from utils import tcpThread
from motorsGUI import MotorsGUI
import gamepad
from utils import clienttcp, frames, echoThread


AXIS_MOTORS = {
    1: 5,  #  left engine
    4: 6,  #  right engine
}

BUTTONS_MOTORS = {
    4: [(1, 50), (2, 50), (3, 50), (4, 50)],  #  up
    5: [(1, -50), (2, -50), (3, -50), (4, -50)],  #  down
    11: [(1, -50), (2, -50), (3, 50), (4, 50)],  #  tilt forward
    12: [(1, 50), (2, 50), (3, -50), (4, -50)],  # tilt backward
    13: [(1, -50), (2, 50), (3, -50), (4, 50)],  # tilt left
    14: [(1, 50), (2, -50), (3, 50), (4, -50)],  #  tilt right
}

MOTORS_VALUES = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

MOTORS_NUM = 6

class MainWindow(MotorsGUI):
    def __init__(self, host, port, parent = None):
        super(MainWindow, self).__init__(parent)

        self.host = host
        self.port = port

        self.thread = echoThread.echoThread(self, self.host, self.port)
        self.thread.connectionState.connect(self.initParams)
        self.thread.start()

        self.startBtn.clicked.connect(self.start)
        #self.bgThread = tcpThread.tcpThread(self, paramsDict, self.host, self.port)
        #self.bgThread.paramsRetrived.connect(self.updateValues)
        #self.bgThread.start()

        self.gamepad = gamepad.joystickThread()
        self.gamepad.setAxes(AXIS_MOTORS.keys())
        self.gamepad.setButtons(BUTTONS_MOTORS.keys())
        self.gamepad.newState.connect(self.sendMotorsValues)

    def initParams(self, connected):
        if not connected:
            self.log.append("Error while connection with robot")
        else:
            self.log.append("Connection with robot established")
            self.getCurrentMotorsValues()

    def getCurrentMotorsValues(self):
        try:
            values = frames.getAllValues(self.host, self.port, "M")
            self.updateValuesGUI(values)
            self.updateValues(values)
        except Exception as e:
            self.log.append(str(e))

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

    def updateValuesGUI(self, params):
        print params
        num = 1
        for param in  params:
            labelValue = getattr(self, "labelValueM" + str(num))
            labelValue.setText(str(param))
            num+=1

    def updateValues(self, values):
        num = 1
        for param in values:
            MOTORS_VALUES[num] = param
            num+=1

    def showMotorsValue(self, axe, value):
        self.log.append(str(axe) + "  " + str(value))

    def sendMotorsValues(self, buttons, axes):
        try:
            self.log.append(buttons)
            self.log.append(axes)
            values = MOTORS_NUM*[0]
            for button in buttons:
                if buttons[button] == 1 and button in BUTTONS_MOTORS:
                    for item in BUTTONS_MOTORS[button]:
                        value = MOTORS_VALUES[item[0]] + item[1]
                        values[item[0]-1] = str(value)
            for a in axes:
                if a in AXIS_MOTORS:
                    values[AXIS_MOTORS[a]] = str(axes[a] * 1000)
            values = frames.setAllValues(self.host, self.port, "M", values)
            if values is not None:
                self.updateValuesGUI(values)
                self.updateValues(values)
            else:
                self.thread.start()
        except Exception as e:
            self.log.append(str(e))

if __name__ == "__main__":
    if len(sys.argv)>2:
        HOST, PORT = sys.argv[1], int(sys.argv[2])
    else:
        HOST, PORT = "localhost", 9998
    app = QApplication(sys.argv)
    mainWindow = MainWindow(HOST, PORT)
    mainWindow.show()
    app.exec_()