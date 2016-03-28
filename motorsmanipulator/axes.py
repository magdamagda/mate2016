from OpenGL.GL import *
from PyQt4 import QtGui
from PyQt4.QtOpenGL import *

class AxesWidget(QGLWidget):
    def __init__(self, parent = None):
        super(AxesWidget, self).__init__(parent)
        self.xangle=0
        self.yangle=0
        self.zangle=0

    def paintGL(self):
        self.createRotation()
        glLoadIdentity()
        glColor3f(0.0, 0.0, 1.0)  # x
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(20, 0, 0)
        glEnd()
        #self.createRotation()
        glColor3f(1.0, 0.0, 0.0)  # z
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 20)
        glEnd()
        #self.createRotation()
        glColor3f(0.0, 1.0, 0.0)  # y
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 20, 0)
        glEnd()

    def createRotation(self):
        glRotate(self.xangle, 1.0, 0.0, 0.0)
        glRotate(self.yangle, 0.0, 1.0, 0.0)
        glRotate(self.zangle, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-50, 50, -50, 50, -50.0, 50.0)
        glViewport(0, 0, w, h)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def setRotation(self, x, y, z):
        self.xangle=x
        self.yangle=y
        self.zangle=z
        self.updateGL()

"""if __name__ == '__main__':
    app = QtGui.QApplication(["Winfred's PyQt OpenGL"])
    widget = WfWidget()
    widget.show()
    app.exec_()"""