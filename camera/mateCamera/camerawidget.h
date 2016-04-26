#ifndef CAMERAWIDGET_H
#define CAMERAWIDGET_H

#include <QWidget>
#include <QString>
#include <QVBoxLayout>
#include <QLabel>
#include <QImage>
#include <QPixmap>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <QTcpSocket>
#include <QByteArray>
#include <QNetworkInterface>
#include "streamingthread.h"
#include "opencv2/videoio.hpp"
#include <ctime>

using namespace cv;

class cameraWidget : public QWidget
{
    Q_OBJECT
public:
    explicit cameraWidget(QString host, int udpPport, int tcpPort, int camNum, int w, int h, int fps, QWidget *parent = 0);
    ~cameraWidget();
    bool changeSize(int w, int h);
    bool changeFps(int value);
    void setTCPPort(int port);
    void setUDPPort(int port);
    bool changeResolution(int w, int h);
    void snapshot();
    bool startRecording();
    bool isRecording();
    bool sharpen();
    void startSavingToFile(QString file);
    void stopSavingToFile();

private:
    void setupUi();
    void setIP();
    void changeSettings(int w, int h, int fps, int port, int on);
    void sendTCPframe(QString frame, const char *slot);
    void sendStartFrame();
    void sendEndFrame();
    void startStreaming();

    QVBoxLayout* layout;
    QLabel* canvas;

    int width;
    int height;
    int fps;
    bool recording;
    bool saving;

    int tcpPort;
    int udpPort;
    int camNum;
    QString host;

    QTcpSocket * tcpSocket;
    streamingThread* streaming;

    cv::VideoWriter* videoWriter;
    CvSize realImageSize;

    QMetaObject::Connection* lastConnection;
    //std::time_t lastImageRecord;

signals:

public slots:
    void display(cv::Mat img);
    void save(cv::Mat img);
    void startFrameResponse();
    void endFrameResponse();
    void setIPResponse();
    void setSettingsResponse();
    bool stopRecording();

};

#endif // CAMERAWIDGET_H
