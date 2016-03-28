#include "mainwindow.h"
#include <QApplication>
#include <QString>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QString host = "localhost";
    int udpPort = 1234;
    int tcpPort = 9998;
    int width=640;
    int height=480;
    int fps=30;
    int num = 1;
    if(argc > 3){
        host = argv[1];
        udpPort = atoi(argv[2]);
        num = atoi(argv[3]);
    }
    MainWindow w(host, udpPort, tcpPort, num, width, height, fps);
    w.show();

    return a.exec();
}
