# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import chart

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(716, 656)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.layoutWidget = QtGui.QWidget(self.centralWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 691, 560))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layoutWidget.sizePolicy().hasHeightForWidth())
        self.layoutWidget.setSizePolicy(sizePolicy)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.mainLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.mainLayout.setMargin(11)
        self.mainLayout.setSpacing(6)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.measuresValues = QtGui.QGridLayout()
        self.measuresValues.setMargin(11)
        self.measuresValues.setSpacing(6)
        self.measuresValues.setObjectName(_fromUtf8("measuresValues"))

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.measuresValues.addItem(spacerItem1, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.measuresValues.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.measuresValues.addItem(spacerItem3, 0, 2, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.measuresValues.addItem(spacerItem4, 0, 3, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.measuresValues.addItem(spacerItem5, 1, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.measuresValues.addItem(spacerItem6, 1, 1, 1, 1)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.measuresValues.addItem(spacerItem7, 1, 2, 1, 1)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.measuresValues.addItem(spacerItem8, 1, 3, 1, 1)
        self.measuresValues.setRowMinimumHeight(0, 100)
        self.measuresValues.setRowMinimumHeight(1, 100)
        self.measuresValues.setColumnStretch(0, 1)
        self.measuresValues.setColumnStretch(1, 1)
        self.measuresValues.setColumnStretch(2, 1)
        self.measuresValues.setColumnStretch(3, 1)
        self.measuresValues.setRowStretch(0, 1)
        self.measuresValues.setRowStretch(1, 1)
        self.mainLayout.addLayout(self.measuresValues)
        self.refreshForm = QtGui.QHBoxLayout()
        self.refreshForm.setMargin(11)
        self.refreshForm.setSpacing(6)
        self.refreshForm.setObjectName(_fromUtf8("refreshForm"))
        self.label = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.refreshForm.addWidget(self.label)
        self.spinBoxRefresh = QtGui.QSpinBox(self.layoutWidget)
        self.spinBoxRefresh.setObjectName(_fromUtf8("spinBoxRefresh"))
        self.spinBoxRefresh.setValue(5)
        self.refreshForm.addWidget(self.spinBoxRefresh)
        self.btnSave = QtGui.QPushButton(self.layoutWidget)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.refreshForm.addWidget(self.btnSave)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.refreshForm.addItem(spacerItem7)
        self.mainLayout.addLayout(self.refreshForm)
        self.chart = QtGui.QHBoxLayout()
        self.chart.setMargin(11)
        self.chart.setSpacing(6)
        self.chart.setObjectName(_fromUtf8("chart"))
        self.chartPlaceholder = chart.MyDynamicMplCanvas(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartPlaceholder.sizePolicy().hasHeightForWidth())
        self.chartPlaceholder.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(71)
        self.chartPlaceholder.setFont(font)
        self.chartPlaceholder.setObjectName(_fromUtf8("chartPlaceholder"))
        self.chart.addWidget(self.chartPlaceholder)
        self.legend = QtGui.QVBoxLayout()
        self.legend.setMargin(11)
        self.legend.setSpacing(6)
        self.legend.setObjectName(_fromUtf8("legend"))
        self.chart.addLayout(self.legend)
        self.mainLayout.addLayout(self.chart)
        self.mainLayout.setStretch(0, 5)
        self.mainLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 716, 25))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Refresh:", None))
        self.btnSave.setText(_translate("MainWindow", "Save", None))
        #self.chartPlaceholder.setText(_translate("MainWindow", "Chart here", None))