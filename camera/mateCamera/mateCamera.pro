#-------------------------------------------------
#
# Project created by QtCreator 2016-03-17T19:15:32
#
#-------------------------------------------------

QT       += core gui
QT       += network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = mateCamera
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    camerawidget.cpp \
    streamingthread.cpp \
    PracticalSocket.cpp

HEADERS  += mainwindow.h \
    camerawidget.h \
    streamingthread.h \
    PracticalSocket.h

FORMS    += mainwindow.ui

INCLUDEPATH += /usr/local/include/opencv2
LIBS += -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui
LIBS += -lopencv_imgproc
LIBS += -lopencv_ml
LIBS += -lopencv_video
LIBS += -lopencv_features2d
LIBS += -lopencv_calib3d
LIBS += -lopencv_objdetect
LIBS += -lopencv_contrib
LIBS += -lopencv_legacy
LIBS += -lopencv_flann
LIBS += -lopencv_videoio

CONFIG += c++11
