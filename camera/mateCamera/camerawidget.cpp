#include "camerawidget.h"

cameraWidget::cameraWidget(QString host, int udpPort, int tcpPort, int camNum, int w, int h, int fps, QWidget *parent) :
    QWidget(parent), host(host), udpPort(udpPort), tcpPort(tcpPort), camNum(camNum), width(w), height(h), fps(fps)
{
    streaming=nullptr;
    recording = false;
    setupUi();
    setIP();
}

void cameraWidget::setupUi(){
    layout = new QVBoxLayout(this);
    canvas = new QLabel("Camera image here");
    layout->addWidget(canvas);
}

void cameraWidget::display(Mat img)
{
    cv::cvtColor(img, img, CV_RGB2BGR);
    QImage qimage((uchar*)img.data, img.cols, img.rows, img.step, QImage::Format_RGB888);
    this->canvas->setPixmap(QPixmap::fromImage(qimage));
}

void cameraWidget::sendTCPframe(QString frame, const char* slot){
    QByteArray data = frame.toUtf8();
    tcpSocket = new QTcpSocket(this);
    connect(tcpSocket, SIGNAL(readyRead()),this, slot);
    tcpSocket->connectToHost(this->host, this->tcpPort);
    if(!tcpSocket->waitForConnected(5000))
    {
        cout << tcpSocket->errorString().toStdString();
    }
    else{
        cout<<"sended: " << frame.toStdString()<<endl;
        tcpSocket->write(data);
    }
}

void cameraWidget::sendStartFrame(){
    sendTCPframe("(S,C," + QString::number(this->camNum) + ",1)", SLOT(startFrameResponse()));
}

void cameraWidget::sendEndFrame(){
    sendTCPframe("(S,C," + QString::number(this->camNum) + ",0)", SLOT(endFrameResponse()));
}

void cameraWidget::setIP(){
    foreach (const QHostAddress &address, QNetworkInterface::allAddresses()) {
        if (address.protocol() == QAbstractSocket::IPv4Protocol && address != QHostAddress(QHostAddress::LocalHost))
             sendTCPframe("(S,C,H," + address.toString() + ")", SLOT(setIPResponse()));
    }
}

void cameraWidget::changeSettings(int w, int h, int fps, int port, int on){
    sendTCPframe("(S,C," + QString::number(this->camNum) + "," + QString::number(w) + "," + QString::number(h) + "," + QString::number(fps) + "," + QString::number(on) + "," + QString::number(port) + ")", SLOT(setSettingsResponse()));
}

void cameraWidget::startFrameResponse(){
    cout<<"start frame response"<<endl;
    QByteArray data = tcpSocket->readAll();
    QString frame(data);
    cout<<frame.toStdString()<<endl;
    startStreaming();
}

void cameraWidget::startStreaming(){
    if (streaming == nullptr){
        cout<<"start streaming"<<endl;
        streaming = new streamingThread(this->host, this->udpPort, this->camNum);
        qRegisterMetaType< cv::Mat >("cv::Mat");
        connect(streaming, SIGNAL(cameraRetrived(cv::Mat)),this, SLOT(display(cv::Mat)));
        streaming->start();
        recording = true;
    }
}

void cameraWidget::endFrameResponse(){
    QByteArray data = tcpSocket->readAll();
    QString frame(data);
}

void cameraWidget::setIPResponse(){
    QByteArray data = tcpSocket->readAll();
    QString frame(data);
}

void cameraWidget::setSettingsResponse(){
    QByteArray data = tcpSocket->readAll();
    QString frame(data);
    cout<<"set settings response "<<frame.toStdString()<<endl;
    int pos1=0;
    int pos2=0;
    pos1 = frame.indexOf("(", pos1);
    pos2 = frame.indexOf(")", pos2);
    int len = pos2-pos1-1;
    frame = frame.mid(pos1+1, len);
    QStringList args = frame.split(',');
    this->width = (args.at(3)).toInt();
    this->height = args.at(4).toInt();
    this->fps = args.at(5).toInt();
    int on = args.at(6).toInt();
    this->udpPort = args.at(7).toInt();
    // set values
    if(on==1){
        startStreaming();
    }
    else{
        sendStartFrame();
    }
}

bool cameraWidget::changeSize(int w, int h){
    changeSettings(w, h, this->fps, this->udpPort, 0);
}

bool cameraWidget::changeFps(int value){
    changeSettings(this->width, this->height, value, this->udpPort, 0);
}

void cameraWidget::setTCPPort(int port){
    this->tcpPort = port;
}

void cameraWidget::setUDPPort(int port){
    stopRecording();
    changeSettings(this->width, this->height, this->fps, this->udpPort, 1);
}

bool cameraWidget::changeResolution(int w, int h){

}

void cameraWidget::snapshot(){

}

bool cameraWidget::startRecording(){
    cout<<"start recording"<<endl;
    if(!recording){
        cout<<"send start frame"<<endl;
        changeSettings(this->width, this->height, this->fps, this->udpPort, 1);
    }
}

bool cameraWidget::stopRecording(){
    cout<<"stop recording"<<endl;
    if(recording){
        cout<<"send end frame"<<endl;
        this->sendEndFrame();
        streaming->stopStreaming();
        streaming->wait();
        delete streaming;
        recording = false;
    }
}

bool cameraWidget::isRecording(){
    return recording;
}

bool cameraWidget::sharpen(){

}

cameraWidget::~cameraWidget(){
    stopRecording();
    delete this->tcpSocket;
}
