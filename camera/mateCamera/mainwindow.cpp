#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QString host, int udpPort, int tcpPort, int num, int w, int h, int fps,  QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    //ui->setupUi(this);
    this->createContextMenu();
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

void MainWindow::contextMenuEvent(QContextMenuEvent *event){
    QMenu menu(this);
    menu.addAction(startRec);
    menu.addAction(stopRec);
    menu.exec(event->globalPos());
}

void MainWindow::createContextMenu(){
    this->startRec = new QAction(tr("&Start recording"), this);
    connect(this->startRec, &QAction::triggered, this, &MainWindow::startRecording);

    this->stopRec = new QAction(tr("&Stop recording"), this);
    connect(this->stopRec, &QAction::triggered, this, &MainWindow::stopRecording);
}

void MainWindow::startRecording(){
    if(camera->isRecording()){
        QFileDialog dialog(this);
        dialog.setFileMode(QFileDialog::AnyFile);
        QString file = dialog.getSaveFileName(this, tr("Choose record directory"), "/home/");
        camera->startSavingToFile(file);
    }
}

void MainWindow::stopRecording(){
    camera->stopSavingToFile();
}

MainWindow::~MainWindow()
{
    delete ui;
    delete camera;
}
