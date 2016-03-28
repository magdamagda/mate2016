import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ManipulatorGUI(QDialog):

    def __init__(self, parent=None):
        super(ManipulatorGUI, self).__init__(parent)

        layout = QVBoxLayout()

        settingsForm = QHBoxLayout()
        self.labelPadNum = QLabel()
        self.labelPadNum.setText("Pad: ")
        settingsForm.addWidget(self.labelPadNum)
        self.inputPadNum = QLineEdit()
        self.inputPadNum.setText("1")
        settingsForm.addWidget(self.inputPadNum)

        self.startBtn = QPushButton("Start")
        settingsForm.addWidget(self.startBtn)

        layout.addItem(settingsForm)

        axesLayout = QHBoxLayout()

        self.addAxeLayout(axesLayout, 1)
        self.addAxeLayout(axesLayout, 2)
        self.addAxeLayout(axesLayout, 3)
        self.addAxeLayout(axesLayout, 4)

        layout.addItem(axesLayout)

        self.saveValuesBtn = QPushButton()
        self.saveValuesBtn.setText("Save values")
        layout.addWidget(self.saveValuesBtn)

        self.log = QTextEdit()
        self.log.resize(100, 100)
        layout.addWidget(self.log)
        self.setLayout(layout)

    def addAxeLayout(self, parent, number):
        layout = QVBoxLayout()

        label = QLabel()
        label.setText("Axe " + str(number))
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

