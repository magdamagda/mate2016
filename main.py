import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess

class Buttons(QDialog):

    def __init__(self, parent=None):
        super(Buttons, self).__init__(parent)

        layout = QVBoxLayout()
        self.addButton(layout, "Camera 1", lambda: self.execProgram(None))
        self.addButton(layout, "Camera 2", lambda: self.execProgram(None))
        self.addButton(layout, "Measures", lambda: self.execProgram([sys.executable, 'measures/main.py']))
        self.addButton(layout, "Manipulator", lambda: self.execProgram(None))
        self.addButton(layout, "Motors", lambda: self.execProgram(None))
        self.addButton(layout, "Test Server TCP", lambda: self.execProgram("gnome-terminal -e sudo servers/servertcp.py", True))
        self.addButton(layout, "Camera test", lambda: self.execProgram("gnome-terminal -e './camera/stream.sh'"))
        self.setLayout(layout)

    def addButton(self, layout, text, fun):
        btn = QPushButton(text)
        btn.clicked.connect(fun)
        layout.addWidget(btn)


    def execProgram(self, command, shell = False):
        #os.system(path)
        pid = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell = shell)

app = QApplication(sys.argv)
buttons = Buttons()
buttons.show()
app.exec_()