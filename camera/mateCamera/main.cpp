#include "mainwindow.h"
#include <QApplication>
#include <QString>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QString host = "192.168.1.170";
    int udpPort = 1234;
    int tcpPort = 6001;
    int width=640;
    int height=480;
    int fps=15;
    int num = 0;
    if(argc > 7){
        host = argv[1];
        udpPort = atoi(argv[2]);
        tcpPort = atoi(argv[3]);
        num = atoi(argv[4]);
        width= atoi(argv[5]);
        height= atoi(argv[6]);
        fps= atoi(argv[7]);
    }

    MainWindow w(host, udpPort, tcpPort, num, width, height, fps);
    w.show();

    return a.exec();
}
