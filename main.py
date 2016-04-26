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

        self.addCameraButton(layout, "Camera 0", 'camera/build-mateCamera-Desktop_Qt_5_5_1_GCC_64bit-Debug/mateCamera', 6001, 1234, 0)
        self.addCameraButton(layout, "Camera 1", 'camera/build-mateCamera-Desktop_Qt_5_5_1_GCC_64bit-Debug/mateCamera', 6002, 1235, 1)
        self.addButton(layout, "Measures", 'measures/main.py', 6004)
        self.addButton(layout, "Control panel", 'controlManagament/main.py', 6003)
        self.setLayout(layout)

    def addButton(self, layout, text, command, defaultPort = "6003"):
        l = QHBoxLayout()
        btn = QPushButton(text)
        l.addWidget(btn)
        portInput = QLineEdit()
        portInput.setText(str(defaultPort))
        l.addWidget(portInput)
        btn.clicked.connect(lambda:  self.execProgram([sys.executable, command, self.ipNum.text(), portInput.text()]))
        layout.addItem(l)

    def addCameraButton(self, layout, text, command, tcpPort, udpPort, num, height = 480, width = 640, fps=30):
        l = QHBoxLayout()
        btn = QPushButton(text)
        l.addWidget(btn)

        portInput = QLineEdit()
        portInput.setText(str(tcpPort))
        l.addWidget(portInput)

        udpInput = QLineEdit()
        udpInput.setText(str(udpPort))
        l.addWidget(udpInput)

        heightInput = QLineEdit()
        heightInput.setText(str(height))
        l.addWidget(heightInput)

        widthInput = QLineEdit()
        widthInput.setText(str(width))
        l.addWidget(widthInput)

        fpsInput = QLineEdit()
        fpsInput.setText(str(fps))
        l.addWidget(fpsInput)

        btn.clicked.connect(lambda:  self.execProgram([command, self.ipNum.text(), udpInput.text(),
                                                       portInput.text(), str(num), widthInput.text(), heightInput.text(),
                                                       fpsInput.text()]))
        layout.addItem(l)


    def execProgram(self, command, shell = False):
        #os.system(path)
        print str(command)
        pid = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell = shell)

app = QApplication(sys.argv)
buttons = Buttons()
buttons.show()
app.exec_()