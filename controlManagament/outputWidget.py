from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class OutputWidget(QDialog):

    stateChanged = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(OutputWidget, self).__init__(parent)

        self.layout = QVBoxLayout()

        self.addOutput("output 0", 0, self.layout)
        self.addOutput("output 1", 1, self.layout)
        self.addOutput("output 2", 2, self.layout)

        self.setLayout(self.layout)

    def addOutput(self, name, num, layout):
        l = QHBoxLayout()
        setattr(self, "label" + str(num), QLabel())
        label = getattr(self, "label" + str(num))
        label.setText(name)
        l.addWidget(label)

        setattr(self, "output" + str(num), QCheckBox())
        input = getattr(self, "output" + str(num))
        input.stateChanged.connect(lambda: self.stateChanged.emit(num, input.checkState()))

        l.addWidget(input)

        layout.addItem(l)

    def updateState(self, num, state):
        self.blockSignals(True)
        input = getattr(self, "output" + str(num))
        input.setChecked(state)
        self.blockSignals(False)
