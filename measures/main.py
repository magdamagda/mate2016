import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

"""from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis"""


import mainGUI
import tcpThread
import chart
import datetime

# param name and unit
paramsUnits = {"T" : "C", "P" : "Pa"}
paramsList = [("T", 1), ("P", 1), ("T", 2), ("T", 3), ("T", 4)]
paramsValues = {}

#alarms settings
alarmsSettings = {
    "T1": [(None, 30, 1), (20, None, 2)],
}

alarms = {
    1: "Za wysokie T1",
    2: "Za niskie T1"
}

CHART_PARAMS = ["T1", "P1"]

MEASURES_FILE = "measures"

class MainWindow(mainGUI.Ui_MainWindow):
    def __init__(self, host, port, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi()
        self.addAllParams()
        self.addAllCharts()
        self.bgThread = tcpThread.tcpThread(self, paramsList, host, port)
        self.bgThread.paramsRetrived.connect(self.updateValues)
        self.btnSave.clicked.connect(lambda : self.bgThread.setRefresh(self.spinBoxRefresh.value()))
        self.bgThread.start()

    def addAllParams(self):
        x=0
        y=0
        for p in paramsList:
            name = p[0] + str(p[1])
            self.addParam(name, x, y)
            paramsValues[name] = []
            x+=1
            if x==4:
                x=0
                y=(y+1)%2

    def addAllCharts(self):
        x=0
        y=0
        for p in CHART_PARAMS:
            self.addChart(p, x, y)
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


    def addChart(self, name, x, y):
        chartLayout = QVBoxLayout()
        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        chartLayout.addWidget(label)
        setattr(self, "chartParam" + name, chart.MyDynamicMplCanvas())
        chartParam = getattr(self, "chartParam" + name)
        chartLayout.addWidget(chartParam)
        self.charts.addLayout(chartLayout, y, x, 1, 1)

    def drawChart(self):
        try:
            for p in CHART_PARAMS:
                chartParam = getattr(self, "chartParam" + p)
                chartParam.update_figure(paramsValues[p])
        except Exception as e:
            print str(e)

    def updateValues(self, params):
        print "update values"
        print params
        alarmMsg = ""
        for param in  params:
            name = param[0] + param[1]
            value = param[2]
            labelValue = getattr(self, "labelValue" + name)
            labelValue.setText(str(value) + paramsUnits[param[0]])
            self.saveToFile(name, value)
            value = float(value)
            paramsValues[name].append(value)
            if name in alarmsSettings:
                for a in alarmsSettings[name]:
                    if a[0] is not None and a[0]>value:
                        alarmMsg+=alarms[a[2]]
                    elif a[1] is not None and a[1]<value:
                        alarmMsg+=alarms[a[2]]
        self.drawChart()
        self.showAlert(alarmMsg)

    def showAlert(self, message):
        self.alert.setText(message)

    def saveToFile(self, param, value):
        with open(MEASURES_FILE + param, "a") as f:
            f.write(str(datetime.datetime.now()) + "\t")
            f.write(value)
            f.write("\n")

if __name__ == "__main__":
    if len(sys.argv)>2:
        HOST, PORT = sys.argv[1], int(sys.argv[2])
    else:
        HOST, PORT = "localhost", 6003
    app=QApplication(sys.argv)
    form = MainWindow(HOST, PORT)
    form.show()
    app.exec_()