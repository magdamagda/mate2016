# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(QtGui.QDialog):
    def setupUi(self):
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        #self.mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
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
        self.measuresValues.setRowMinimumHeight(0, 50)
        self.measuresValues.setColumnStretch(0, 1)
        self.measuresValues.setColumnStretch(1, 1)
        self.measuresValues.setColumnStretch(2, 1)
        self.measuresValues.setColumnStretch(3, 1)
        self.measuresValues.setRowStretch(0, 1)
        self.mainLayout.addLayout(self.measuresValues)
        self.refreshForm = QtGui.QHBoxLayout()
        self.refreshForm.setMargin(11)
        self.refreshForm.setSpacing(6)
        self.refreshForm.setObjectName(_fromUtf8("refreshForm"))
        self.label = QtGui.QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.refreshForm.addWidget(self.label)
        self.spinBoxRefresh = QtGui.QSpinBox()
        self.spinBoxRefresh.setObjectName(_fromUtf8("spinBoxRefresh"))
        self.spinBoxRefresh.setValue(5)
        self.refreshForm.addWidget(self.spinBoxRefresh)
        self.btnSave = QtGui.QPushButton()
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.refreshForm.addWidget(self.btnSave)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.refreshForm.addItem(spacerItem7)
        self.mainLayout.addLayout(self.refreshForm)
        self.charts = QtGui.QGridLayout()
        self.charts.setMargin(11)
        self.charts.setSpacing(6)
        self.charts.setObjectName(_fromUtf8("chart"))
        self.charts.setRowMinimumHeight(0, 100)

        #sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.chartPlaceholder.sizePolicy().hasHeightForWidth())
        #self.chartPlaceholder.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(71)

        self.mainLayout.addLayout(self.charts)
        self.mainLayout.setStretch(0, 5)
        self.mainLayout.setStretch(1, 1)
        self.alert = QtGui.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
        self.alert.setPalette(palette)
        self.alert.setFont(font)
        self.mainLayout.addWidget(self.alert)

        self.retranslateUi()



    def retranslateUi(self):
        self.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Refresh:", None))
        self.btnSave.setText(_translate("MainWindow", "Save", None))
        #self.chartPlaceholder.setText(_translate("MainWindow", "Chart here", None))