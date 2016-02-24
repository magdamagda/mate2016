from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

"""from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis"""


import mainGUI
from servers import tcpThread
import chart

# param name and unit
paramsDict = {"T1" : "C", "T2" : "C", "T3" : "C"}
paramsValues = {"T1" : [], "T2" : [], "T3" : []}

CHART_FILE = 'chart.png'

class MainWindow(QMainWindow, mainGUI.Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.addAllParams()
        self.bgThread = tcpThread.tcpThread(self, paramsDict.keys())
        self.bgThread.paramsRetrived.connect(self.updateValues)
        self.btnSave.clicked.connect(lambda : self.bgThread.setRefresh(self.spinBoxRefresh.value()))
        self.bgThread.start()

    def addAllParams(self):
        x=0
        y=0
        for p in paramsDict:
            self.addParam(p, x, y)
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

        setattr(self, "labelName" + name, QLabel(self.layoutWidget))
        labelName = getattr(self, "labelName" + name)
        font = QFont()
        font.setPointSize(14)
        labelName.setFont(font)
        labelName.setAlignment(Qt.AlignCenter)
        labelName.setObjectName("labelName" + name)
        measureView.addWidget(labelName)

        setattr(self, "labelValue" + name, QLabel(self.layoutWidget))
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

        setattr(self, "chartParam" + name, QCheckBox(self.layoutWidget))
        chartParam = getattr(self, "chartParam" + name)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(chartParam.sizePolicy().hasHeightForWidth())
        chartParam.setSizePolicy(sizePolicy)
        chartParam.setObjectName("chartParam")
        chartParam.setText(name)
        self.legend.addWidget(chartParam)

    """def drawChart(self):
        # Set the vertical range from 0 to 100
        max_y = 100

        # Chart size of 200x125 pixels and specifying the range for the Y axis
        chart = SimpleLineChart(200, 125, y_range=[0, max_y])

        for param in paramsValues:
            data = paramsValues[param]
            chart.add_data(data)

        # Set the line colour to blue
        chart.set_colours(['0000FF'])

        # Set the vertical stripes
        chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.2, 'FFFFFF', 0.2)

        # Set the horizontal dotted lines
        chart.set_grid(0, 25, 5, 5)

        # The Y axis labels contains 0 to 100 skipping every 25, but remove the
        # first number because it's obvious and gets in the way of the first X
        # label.
        left_axis = list(range(0, max_y + 1, 25))
        left_axis[0] = ''
        chart.set_axis_labels(Axis.LEFT, left_axis)

        # X axis labels
        chart.set_axis_labels(Axis.BOTTOM, \
            ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])

        chart.download(CHART_FILE)
        pixmap = QPixmap(CHART_FILE)
        self.chartPlaceholder.setPixmap(pixmap)"""

    def drawChart(self):
        self.chartPlaceholder.update_figure()

    def updateValues(self, params):
        print "update values"
        for param in  params:
            labelValue = getattr(self, "labelValue" + param)
            labelValue.setText(str(params[param]) + paramsDict[param])
            paramsValues[param].append(params[param])
        #self.drawChart()

app=QApplication(sys.argv)
form = MainWindow()
form.show()
app.exec_()