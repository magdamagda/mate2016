from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ButtonsSettingsWidget(QDialog):

    def __init__(self, parent=None, columns = [0,1,2,3,4,5], rows=["A", "B", "X", "Y","top left", "top right", "axis0", "axis1", "axis2", "axis3", "axis4", "axis5"]):
        super(ButtonsSettingsWidget, self).__init__(parent)

        layout = QVBoxLayout()

        self.table = QGridLayout()

        self.setColsRows(columns, rows)

        self.saveBtn = QPushButton()
        self.saveBtn.setText("Save")
        layout.addItem(self.table)
        layout.addWidget(self.saveBtn)
        self.setLayout(layout)

    def setColsRows(self, columns, rows):
        self.columns = columns
        self.rows = rows

        i=1
        for col in columns:
            h = QLabel()
            h.setText(str(col))
            self.table.addWidget(h, 0, i, 1, 1)
            i+=1

        i=1
        for r in rows:
            h = QLabel()
            h.setText(str(r))
            self.table.addWidget(h, i, 0, 1, 1)
            i+=1

        for i in range(1, len(rows)+1):
            for j in range(1, len(columns) +1):
                setattr(self, str(i) + "_" + str(j), QLineEdit("0"))
                item = getattr(self, str(i) + "_" + str(j))
                self.table.addWidget(item, i, j)


    def getValues(self):
        values = []
        for i in range(1, len(self.rows)+1):
            values.append([])
            for j in range(1, len(self.columns) +1):
                item = getattr(self, str(i) + "_" + str(j))
                value = float(item.text())
                if value!=0:
                    values[i-1].append((self.columns[j-1], value))
        return values

    def setValues(self, values):
        i=1
        for row in values:
            for col in row:
                item = getattr(self, str(i) + "_" + str(col[0]+1))
                item.setText(str(col[1]))
            i+=1