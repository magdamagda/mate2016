import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import manipulatorGUI
import gamepad
import time
from utils import clienttcp, frames, echoThread

AXES_BUTTONS = {
    0: (1, 10),
    1: (1, -10),
    2: (2, 10),
    3: (2, -10),
    4: (3, 10),
    5: (3, -10),
    6: (4, 10),
    7: (4, -10),
}

AXES_NUM = 4

class Manipulator(manipulatorGUI.ManipulatorGUI):
    def __init__(self, host = "localhost", port = 9998, parent=None):
        super(Manipulator, self).__init__(parent)

        self.host = host
        self.port = port

        self.thread = echoThread.echoThread(self, self.host, self.port)
        self.thread.connectionState.connect(self.initParams)
        self.thread.start()

        self.startBtn.clicked.connect(self.start)
        self.saveValuesBtn.clicked.connect(self.saveVelocity)

        self.gamepad = gamepad.joystickThread()
        self.gamepad.setButtons(AXES_BUTTONS.keys())
        self.gamepad.newState.connect(self.sendAxesValues)

    def initParams(self, connected):
        if not connected:
            self.log.append("Error while connection with robot")
        else:
            self.log.append("Connection with robot established")
            self.getCurrentAxesPos()
            self.getCurrentAxesVelocity()

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

    def sendAxesValues(self, buttons, axes):
        try:
            self.log.append(buttons)
            values = AXES_NUM*[0]
            for button in buttons:
                if buttons[button] == 1 and button in AXES_BUTTONS:
                    ax = AXES_BUTTONS[button][0]
                    pos = AXES_BUTTONS[button][1]
                    values[ax-1] = str(pos)
            positions = frames.setAllValues(self.host, self.port, "A", values)
            if positions is not None:
                self.showAxesPos(positions)
            else:
                self.thread.start()
        except Exception as e:
            self.log.append(str(e))

    def getCurrentAxesPos(self):
        positions = frames.getAllValues(self.host, self.port, "A")
        if positions is not None:
            self.showAxesPos(positions)

    def getCurrentAxesVelocity(self):
        velocity = frames.getAxesVelocity(self.host, self.port)
        if velocity is not None:
            self.showAxesVelocity(velocity)

    def showAxesVelocity(self, velocity):
        num = 1
        for v in velocity:
            l=getattr(self, "velocity" + str(num))
            l.setValue(v)
            num=num + 1

    def showAxesPos(self, positions):
        num = 1
        for v in positions:
            l=getattr(self, "position" + str(num))
            l.setText(str(v))
            num=num + 1

    def saveVelocity(self):
        values = []
        for i in range(1,AXES_NUM+1):
            l=getattr(self, "velocity" + str(i))
            values.append(str(l.value()))
        frames.setAxesVelocity(self.host, self.port, values)

if __name__ == "__main__":
    if len(sys.argv)>2:
        HOST, PORT = sys.argv[1], int(sys.argv[2])
    else:
        HOST, PORT = "localhost", 9998
    app = QApplication(sys.argv)
    mainWindow = Manipulator(HOST, PORT)
    mainWindow.show()
    app.exec_()