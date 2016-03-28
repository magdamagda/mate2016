import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ManipulatorGUI(QDialog):

    def __init__(self, parent=None):
        super(ManipulatorGUI, self).__init__(parent)

        layout = QVBoxLayout()
        self.btnStart = QPushButton("Start")
        layout.addWidget(self.btnStart)
        self.log = QTextEdit()
        self.log.resize(100, 100)
        layout.addWidget(self.log)
        self.setLayout(layout)


