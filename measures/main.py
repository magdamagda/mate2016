import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

"""from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis"""


import mainGUI
import tcpThread

# param name and unit
paramsUnits = {"T" : "C", "P" : "Pa"}
paramsList = ["T", "P"]
paramsValues = {"T" : [], "P" : []}

class MainWindow(mainGUI.Ui_MainWindow):
    def __init__(self, host, port, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi()
        self.addAllParams()
        self.bgThread = tcpThread.tcpThread(self, paramsList, host, port)
        self.bgThread.paramsRetrived.connect(self.updateValues)
        self.btnSave.clicked.connect(lambda : self.bgThread.setRefresh(self.spinBoxRefresh.value()))
        self.bgThread.start()

    def addAllParams(self):
        x=0
        y=0
        for p in paramsList:
            self.addParam(p[0], x, y)
            x+=1
            if x==4:
                x=0
                y=(y+1)%2

    def addParam(self, name, posX, posY):
        setattr(self, "measureView" + name, QVBoxLayout())
        measureView = getattr(self, "measureView" + name)
        measureView.setMargin(11)
        measureView.setSpacing(6)
        measureView.setObjectName("measureView" + name)

        setattr(self, "labelName" + name, QLabel())
        labelName = getattr(self, "labelName" + name)
        font = QFont()
        font.setPointSize(14)
        labelName.setFont(font)
        labelName.setAlignment(Qt.AlignCenter)
        labelName.setObjectName("labelName" + name)
        measureView.addWidget(labelName)

        setattr(self, "labelValue" + name, QLabel())
        labelValue = getattr(self, "labelValue" + name)
        font = QFont()
        font.setFamily("Droid Sans")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        labelValue.setFont(font)
        labelValue.setStyleSheet("background-color: rgb(145, 199, 222);")
        labelValue.setFrameShape(QFrame.NoFrame)
        labelValue.setFrameShadow(QFrame.Plain)
        labelValue.setTextFormat(Qt.AutoText)
        labelValue.setAlignment(Qt.AlignCenter)
        labelValue.setObjectName("labelValue" + name)
        labelName.setText(name)
        labelValue.setText("---")
        measureView.addWidget(labelValue)
        measureView.setStretch(0, 1)
        measureView.setStretch(1, 3)
        self.measuresValues.addLayout(measureView, posY, posX, 1, 1)

        setattr(self, "chartParam" + name, QCheckBox())
        chartParam = getattr(self, "chartParam" + name)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(chartParam.sizePolicy().hasHeightForWidth())
        chartParam.setSizePolicy(sizePolicy)
        chartParam.setObjectName("chartParam")
        chartParam.setText(name)
        self.legend.addWidget(chartParam)

    def drawChart(self):
        self.chartPlaceholder.update_figure(paramsValues["T"], paramsValues["P"])

    def updateValues(self, params):
        print "update values"
        print params
        for param in  params:
            labelValue = getattr(self, "labelValue" + param)
            labelValue.setText(str(params[param]) + paramsUnits[param])
            paramsValues[param].append(params[param])
        self.drawChart()

if __name__ == "__main__":
    if len(sys.argv)>2:
        HOST, PORT = sys.argv[1], int(sys.argv[2])
    else:
        HOST, PORT = "localhost", 6003
    app=QApplication(sys.argv)
    form = MainWindow(HOST, PORT)
    form.show()
    app.exec_()