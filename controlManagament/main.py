import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import gui
import gamepad, commThread, queue
import time
from utils import clienttcp, frames, echoThread

BUTTONS_AXIS = {
    0: [(0, 10)],
    1: [(1, 10)],
    2: [(1, -10)],
    3: [(0, -10)],
    4: [],
    5: []
}

AXIS_AXIS = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: []
}

AXIS_NUM = 3

AXIS_MOTORS = {
    0: [],
    1: [(4, 100), (5, 100)], # forward/ back
    2: [],
    3: [(4, 100), (5, -100)], # rotate
    4: [],
    5: []
}

BUTTONS_MOTORS = {
    0: [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)],  # tilt backward
    1: [(0, -5), (1, -5), (2, -5), (3, -5), (4, -5), (5, -5)],  #  tilt right
    2: [(0, -5), (1, 5), (2, -5), (3, 5)],  # tilt left
    3: [(0, -5), (1, -5), (2, 5), (3, 5)],  #  tilt forward
    4: [(0, 5), (1, 5), (2, 5), (3, 5)],  #  up
    5: [(0, -5), (1, -5), (2, -5), (3, -5)],  #  down
}

MOTORS_VALUES = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}

MOTORS_NUM = 6

SAFETY_KEY = 8

UPTIME_INTERVAL = 6000

class ControlManagement(gui.ControlGUI):

    def __init__(self, host = "localhost", port = 6003, parent=None):
        super(ControlManagement, self).__init__(parent)
        self.FRAMES_DICT = {
            'A' : self.showAxesValues,
            'M' : self.setMotorsValues,
            'S' : self.setResponse,
            'O' : self.outputResponse
        }

        self.buttonsSettingsMotors.saveBtn.clicked.connect(self.saveButtonsSettingsMotors)
        self.buttonsSettingsManipulator.saveBtn.clicked.connect(self.saveButtonsSettingsManipulator)
        self.stopMotorsBtn.clicked.connect(self.stopMotors)
        self.modeOnBtn.clicked.connect(self.arm)
        self.modeOffBtn.clicked.connect(self.disarm)
        self.outputsControl.stateChanged.connect(self.setOutput)

        self.host = host
        self.port = port
        self.q = queue.queue()
        self.timer = QTimer()
        self.timer.setInterval(UPTIME_INTERVAL)
        self.timer.timeout.connect(self.sendUptime)

        self.thread = echoThread.echoThread(self, self.host, self.port)
        self.thread.connectionState.connect(self.initParams)
        self.thread.start()

        self.initMotorsControl()
        self.initManipulatorControl()

    def initParams(self, connected):
        if not connected:
            self.log.append("Error while connecting with robot")
        else:
            self.log.append("Connection with robot established")
            self.startCommThread()
            self.startUptime()
            self.getCurrentAxesPos()
            self.getCurrentAxesVelocity()
            self.getCurrentMotorsValues()

    def startCommThread(self):
        self.comm = commThread.commThread(self.q, self.host, self.port)
        self.comm.frameRecived.connect(self.parseFrame)
        self.comm.error.connect(self.commThreadError)
        self.comm.start()

    def parseFrame(self, f):
        try:
            t, data = frames.getFrameTypeAndData(f)
            if str(t) in self.FRAMES_DICT:
                self.FRAMES_DICT[str(t)](data)
            else:
                self.log.append("unknown frame " + t)
        except Exception as e:
            self.log.append(str(e))

    def commThreadError(self, e):
        self.log.append(e)
        if e in []:
            self.comm.stop()
            self.timer.stop()
            self.q._q.clear()
            self.thread.start()

    def initMotorsControl(self):
        self.buttonsSettingsMotors.setValues(BUTTONS_MOTORS.values() + AXIS_MOTORS.values())

        self.startBtnMotor.clicked.connect(self.startMotorPad)

        self.gamepadMotor = gamepad.joystickThread()
        self.gamepadMotor.setAxes(AXIS_MOTORS.keys())
        self.gamepadMotor.setButtons(BUTTONS_MOTORS.keys() + [SAFETY_KEY])
        self.gamepadMotor.newState.connect(self.sendMotorsValues)

    def initManipulatorControl(self):
        self.buttonsSettingsManipulator.setValues(BUTTONS_AXIS.values() + AXIS_AXIS.values())
        self.startBtnManipulator.clicked.connect(self.startManipulatorPad)
        self.saveValuesBtn.clicked.connect(self.saveAxesVelocity)

        self.gamepadManipulator = gamepad.joystickThread()
        self.gamepadManipulator.setButtons(BUTTONS_AXIS.keys())
        self.gamepadManipulator.newState.connect(self.sendAxesValues)

    def startManipulatorPad(self):
        if self.gamepadManipulator.isRunning():
            self.gamepadManipulator.finish()
            self.startBtnManipulator.setText("Start")
        else:
            self.initGamepad(self.gamepadManipulator, int(self.inputPadNumManipulator.text()))
            if self.gamepadManipulator.isRunning():
                self.startBtnManipulator.setText("Stop")

    def startMotorPad(self):
        if self.gamepadMotor.isRunning():
            self.q.push(frames.changeModeFrame(0))
            self.gamepadMotor.finish()
            self.startBtnMotor.setText("Start")
        else:
            self.initGamepad(self.gamepadMotor, int(self.inputPadNumMotor.text()))
            if self.gamepadMotor.isRunning():
                self.startBtnMotor.setText("Stop")

    def initGamepad(self, pad, joystickNum):
        self.log.append("init gamepad")
        try:
            pad.init(joystickNum)
            self.log.append("Joystick connected " + str(joystickNum))
            pad.start()
        except Exception as e:
            print str(e)
            self.log.append(str(e))

    def sendAxesValues(self, buttons, axes):
        self.log.append(str(buttons))
        values = AXIS_NUM * [0]
        for button in buttons:
            if buttons[button] == 1 and button in BUTTONS_AXIS:
                for item in BUTTONS_AXIS[button]:
                    value = item[1] * buttons[button]
                    values[item[0]] += value
        self.q.push(frames.setAllValuesFrame("A", values))

    def getCurrentAxesPos(self):
        self.q.push(frames.getAllValuesFrame("A"))

    def getCurrentAxesVelocity(self):
        self.q.push(frames.getAxesVelocityFrame())

    def showAxesValues(self, data):
        if data[0] == "s" and data[1] == "*":
            self.showAxesVelocity([int(x) for x in data[2:]])
        if data[0] == "*":
            self.showAxesPos([int(x) for x in data[1:]])

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

    def saveAxesVelocity(self):
        values = []
        for i in range(0, AXIS_NUM):
            l=getattr(self, "velocity" + str(i))
            values.append(str(l.value()))
        self.q.push(frames.setAxesVelocityFrame(values))

    def updateMotorValuesGUI(self, params):
        print params
        num = 1
        for param in  params:
            labelValue = getattr(self, "labelValueM" + str(num))
            labelValue.setText(str(param))
            num+=1

    def updateMotorValues(self, values):
        self.log.append(str(values))
        global MOTORS_VALUES
        num = 0
        for param in values:
            MOTORS_VALUES[num] = param
            num+=1
        self.log.append(str(MOTORS_VALUES))

    def sendMotorsValues(self, buttons, axes):
        # self.log.append(str(buttons))
        # self.log.append(str(axes))
        self.log.append("past values")
        self.log.append(str(MOTORS_VALUES))
        values = MOTORS_VALUES.values()
        for button in buttons:
            if button==SAFETY_KEY and buttons[button]==1:
                self.q.urgentFrame(frames.changeModeFrame(0))
            elif button in BUTTONS_MOTORS:
                for item in BUTTONS_MOTORS[button]:
                    value = item[1] * buttons[button]
                    values[item[0]] += value
        for a in axes:
            if a in AXIS_MOTORS:
                for item in AXIS_MOTORS[a]:
                    values[item[0]] += axes[a] * item[1]
        self.log.append(str(values))
        self.q.push(frames.setAllValuesFrame("M", values))

    def stopMotors(self):
        self.q.push(frames.setAllValuesFrame("M", [0,0,0,0,0,0]))

    def setMotorsValues(self, data):
        if data[0]=="*":
            self.updateMotorValues([int(x) for x in data[1:]])
            self.updateMotorValuesGUI([int(x) for x in data[1:]])

    def getCurrentMotorsValues(self):
        self.q.push(frames.getAllValuesFrame("M"))

    def saveButtonsSettingsMotors(self):
        values = self.buttonsSettingsMotors.getValues()
        print values
        global BUTTONS_MOTORS
        for btn in BUTTONS_MOTORS:
            BUTTONS_MOTORS[btn] = values[btn]
        global AXIS_MOTORS
        for axis in AXIS_MOTORS:
            AXIS_MOTORS[axis] = values[6+axis]

        print BUTTONS_MOTORS
        print AXIS_MOTORS


    def saveButtonsSettingsManipulator(self):
        values = self.buttonsSettingsManipulator.getValues()
        print values
        global BUTTONS_AXIS
        for btn in BUTTONS_AXIS:
            BUTTONS_AXIS[btn] = values[btn]
        global AXIS_AXIS
        for axis in AXIS_AXIS:
            AXIS_AXIS[axis] = values[6+axis]

    def setResponse(self, data):
        if data[0]=="m":
            self.log.append("mode " + data[1])

    def arm(self):
        print "arm"
        self.q.push(frames.changeModeFrame(1))

    def disarm(self):
        self.q.urgentFrame(frames.changeModeFrame(0))

    def startUptime(self):
        if not self.timer.isActive():
            self.timer.start()

    def sendUptime(self):
        self.q.push(frames.uptimeFrame())

    def setOutput(self, num, state):
        self.q.push(frames.outputStateFrame(num, state))

    def outputResponse(self, data):
        self.log.append(str(data))

if __name__ == "__main__":
    if len(sys.argv)>2:
        HOST, PORT = sys.argv[1], int(sys.argv[2])
    else:
        HOST, PORT = "192.168.1.170", 6003
    app = QApplication(sys.argv)
    mainWindow = ControlManagement(HOST, PORT)
    mainWindow.show()
    app.exec_()