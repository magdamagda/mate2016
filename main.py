import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess

class Buttons(QDialog):

    def __init__(self, parent=None):
        super(Buttons, self).__init__(parent)

        layout = QVBoxLayout()

        ipLayout = QHBoxLayout()
        ipLayout.addWidget(QLabel("ip: "))
        self.ipNum = QLineEdit()
        self.ipNum.setText("localhost")
        ipLayout.addWidget(self.ipNum)
        layout.addItem(ipLayout)

        self.addButton(layout, "Camera 1", None)
        self.addButton(layout, "Camera 2", None)
        self.addButton(layout, "Measures", 'measures/main.py')
        self.addButton(layout, "Manipulator", 'motorsmanipulator/manipulatorsMain.py')
        self.addButton(layout, "Motors", 'motorsmanipulator/motorsMain.py')
        self.addButton(layout, "Test Server TCP", "gnome-terminal -e sudo utils/servertcp.py")
        self.addButton(layout, "Camera test", None)
        self.setLayout(layout)

    def addButton(self, layout, text, command, defaultPort = "9998"):
        l = QHBoxLayout()
        btn = QPushButton(text)
        l.addWidget(btn)
        portInput = QLineEdit()
        portInput.setText(defaultPort)
        l.addWidget(portInput)
        btn.clicked.connect(lambda:  self.execProgram([sys.executable, command, self.ipNum.text(), portInput.text()]))
        layout.addItem(l)


    def execProgram(self, command, shell = False):
        #os.system(path)
        pid = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell = shell)

app = QApplication(sys.argv)
buttons = Buttons()
buttons.show()
app.exec_()