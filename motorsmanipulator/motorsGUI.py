import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from axes import AxesWidget

class MotorsGUI(QDialog):

    def __init__(self, parent=None):
        super(MotorsGUI, self).__init__(parent)
        self.resize(500, 456)
        layout = QVBoxLayout()

        font = QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)

        self.axesLayout = QHBoxLayout()
        self.axes = AxesWidget()
        self.axesLayout.addWidget(self.axes)
        self.imuLayout = QGridLayout()
        self.addLabel("ax", 0, 0, font, self.imuLayout, "x: ")
        self.addLabel("ay", 1, 0, font, self.imuLayout, "y: ")
        self.addLabel("az", 2, 0, font, self.imuLayout, "z: ")
        self.addLabel("AX", 0, 1, font, self.imuLayout)
        self.addLabel("AY", 1, 1, font, self.imuLayout)
        self.addLabel("AZ", 2, 1, font, self.imuLayout)
        self.axesLayout.addItem(self.imuLayout)
        layout.addItem(self.axesLayout)
        #layout.addWidget(self.axes)

        self.measuresValues = QGridLayout()

        self.addLabel("M1", 0, 0, font, self.measuresValues)
        self.addLabel("M2", 0, 1, font, self.measuresValues)
        self.addLabel("M3", 1, 0, font, self.measuresValues)
        self.addLabel("M4", 1, 1, font, self.measuresValues)
        self.addLabel("M5", 2, 0, font, self.measuresValues)
        self.addLabel("M6", 2, 1, font, self.measuresValues)

        layout.addItem(self.measuresValues)

        self.settingsForm = QHBoxLayout()
        self.labelPadNum = QLabel()
        self.labelPadNum.setText("Pad: ")
        self.settingsForm.addWidget(self.labelPadNum)
        self.inputPadNum = QLineEdit()
        self.inputPadNum.setText("0")
        self.settingsForm.addWidget(self.inputPadNum)

        self.startBtn = QPushButton("Start")
        self.settingsForm.addWidget(self.startBtn)

        spacerItem7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #self.controlTypeForm.addItem(spacerItem7)
        self.settingsForm.addItem(spacerItem7)

        layout.addItem(self.settingsForm)

        self.log =  QTextEdit()
        #self.log.setFixedHeight()
        layout.addWidget(self.log)

        self.setLayout(layout)

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

    def setAxes(self, x, y, z):
        self.axes.setRotation(x, y, z)
