import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from buttonsSettingsWidget import ButtonsSettingsWidget
from outputWidget import OutputWidget

class ControlGUI(QDialog):

    def __init__(self, parent=None):
        super(ControlGUI, self).__init__(parent)

        layout = QHBoxLayout()

        self.addManipulatorControl(layout)
        self.addMotorsControl(layout)

        other = QVBoxLayout()

        self.log =  QTextEdit()
        self.log.setMinimumHeight(200)
        self.log.setMinimumWidth(400)
        #layout.addWidget(self.log)
        other.addWidget(self.log)

        self.outputsControl = OutputWidget()
        #layout.addWidget(self.outputsControl)
        other.addWidget(self.outputsControl)

        layout.addItem(other)

        self.setLayout(layout)

    def addMotorsControl(self, parentLayout):
        layout = QVBoxLayout()

        font = QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)

        self.measuresValues = QGridLayout()

        self.addLabel("M1", 0, 0, font, self.measuresValues)
        self.addLabel("M2", 0, 1, font, self.measuresValues)
        self.addLabel("M3", 1, 0, font, self.measuresValues)
        self.addLabel("M4", 1, 1, font, self.measuresValues)
        self.addLabel("M5", 2, 0, font, self.measuresValues)
        self.addLabel("M6", 2, 1, font, self.measuresValues)

        layout.addItem(self.measuresValues)

        self.stopMotorsBtn = QPushButton("Stop motors")
        layout.addWidget(self.stopMotorsBtn)

        modeLayout = QHBoxLayout()
        self.modeOnBtn = QPushButton("Arm")
        modeLayout.addWidget(self.modeOnBtn)
        self.modeOffBtn = QPushButton("Disarm")
        modeLayout.addWidget(self.modeOffBtn)
        layout.addItem(modeLayout)

        settingsForm = QHBoxLayout()
        self.labelPadNumMotor = QLabel()
        self.labelPadNumMotor.setText("Pad: ")
        settingsForm.addWidget(self.labelPadNumMotor)
        self.inputPadNumMotor = QLineEdit()
        self.inputPadNumMotor.setText("0")
        settingsForm.addWidget(self.inputPadNumMotor)

        self.startBtnMotor = QPushButton("Start")
        settingsForm.addWidget(self.startBtnMotor)

        spacerItem7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #self.controlTypeForm.addItem(spacerItem7)
        settingsForm.addItem(spacerItem7)

        layout.addItem(settingsForm)

        #self.log =  QTextEdit()
        #self.log.setFixedHeight()
        #layout.addWidget(self.log)

        self.buttonsSettingsMotors = ButtonsSettingsWidget() # self, [0,1,2,3,4,5], ["A", "B", "Y", "X", "axis0", "axis1", "axis2", "axis3", "axis4", "axis5"])
        layout.addWidget(self.buttonsSettingsMotors)

        parentLayout.addItem(layout)

    def addManipulatorControl(self, parentLayout):
        layout = QVBoxLayout()

        settingsForm = QHBoxLayout()
        self.labelPadNumManipulator = QLabel()
        self.labelPadNumManipulator.setText("Pad: ")
        settingsForm.addWidget(self.labelPadNumManipulator)
        self.inputPadNumManipulator = QLineEdit()
        self.inputPadNumManipulator.setText("1")
        settingsForm.addWidget(self.inputPadNumManipulator)

        self.startBtnManipulator = QPushButton("Start")
        settingsForm.addWidget(self.startBtnManipulator)

        layout.addItem(settingsForm)

        axesLayout = QHBoxLayout()

        self.addAxeLayout(axesLayout, 0)
        self.addAxeLayout(axesLayout, 1)
        self.addAxeLayout(axesLayout, 2)
        #self.addAxeLayout(axesLayout, 3)

        layout.addItem(axesLayout)

        self.saveValuesBtn = QPushButton()
        self.saveValuesBtn.setText("Save values")
        layout.addWidget(self.saveValuesBtn)

        #self.log = QTextEdit()
        #self.log.resize(100, 100)
        #layout.addWidget(self.log)

        self.buttonsSettingsManipulator = ButtonsSettingsWidget(columns = [0,1,2,3]) # self, [0,1,2,3,4,5], ["A", "B", "Y", "X", "axis0", "axis1", "axis2", "axis3", "axis4", "axis5"])
        layout.addWidget(self.buttonsSettingsManipulator)

        parentLayout.addItem(layout)

    def addAxeLayout(self, parent, number):
        layout = QVBoxLayout()

        label = QLabel()
        label.setText("Axis " + str(number))
        layout.addWidget(label)

        labelPosition = QLabel()
        labelPosition.setText("0")
        setattr(self, "position" + str(number), labelPosition)
        layout.addWidget(labelPosition)

        spinBox = QSpinBox()
        spinBox.setValue(0)
        setattr(self, "velocity" + str(number), spinBox)
        layout.addWidget(spinBox)

        parent.addItem(layout)

    def addLabel(self, name, x, y, font, layout, text="0"):
        setattr(self, "labelValue" + name, QLabel())
        label = getattr(self, "labelValue" + name)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setText(text)
        layout.addWidget(label, x, y, 1, 1)

    def setValue(self, name):
        label = getattr(self, "labelValue" + name)
        label.setText(name + "%")