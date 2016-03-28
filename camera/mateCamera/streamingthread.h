#ifndef STREAMINGTHREAD_H
#define STREAMINGTHREAD_H
#include <QThread>
#include <QString>

#include "PracticalSocket.h" // For UDPSocket and SocketException
#include <iostream>          // For cout and cerr
#include <cstdlib>           // For atoi()
#include <opencv2/opencv.hpp>

#define BUF_LEN 65540

#define FRAME_HEIGHT 720
#define FRAME_WIDTH 1280
#define FRAME_INTERVAL (1000/30)
#define PACK_SIZE 4096 //udp pack size; note that OSX limits < 8100 bytes
#define ENCODE_QUALITY 80


using namespace std;

class streamingThread : public QThread
{
    Q_OBJECT
public:
    streamingThread(QString& host, int port, int camNum);
    void stop();

signals:
    void cameraRetrived(cv::Mat image);

public slots:
    void stopStreaming();

private:
    void run();
    void streamImage();

    bool fstop;

    int cameraPort;
    int infoPort;
    QString host;
    int camNum;
};

#endif // STREAMINGTHREAD_H
