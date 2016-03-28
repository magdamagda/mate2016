#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QString>
#include <QVBoxLayout>
#include <camerawidget.h>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QString host, int udpPort, int tcpPort, int num, int w, int h, int fps, QWidget *parent = 0);
    ~MainWindow();

protected:
    void closeEvent(QCloseEvent *event);

private:
    Ui::MainWindow *ui;
    QWidget *centralWidget;
    QVBoxLayout* mainLayout;
    cameraWidget* camera;
};

#endif // MAINWINDOW_H
