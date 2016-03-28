#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QString host, int udpPort, int tcpPort, int num, int w, int h, int fps,  QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    //ui->setupUi(this);
    this->setWindowTitle("Camera " + QString::number(num));
    centralWidget = new QWidget(this);
    this->setCentralWidget( centralWidget );
    mainLayout = new QVBoxLayout(centralWidget);
    camera = new cameraWidget(host, udpPort, tcpPort, num, w, h, fps, this);
    mainLayout->addWidget(camera);
    //this->setLayout(layout);
    camera->startRecording();
}

void MainWindow::closeEvent(QCloseEvent *event) {

}

MainWindow::~MainWindow()
{
    delete ui;
    delete camera;
}
