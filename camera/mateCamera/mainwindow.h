#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QString>
#include <QVBoxLayout>
#include <camerawidget.h>
#include <QAction>
#include <QContextMenuEvent>
#include <QFileDialog>

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
    void contextMenuEvent(QContextMenuEvent *event) Q_DECL_OVERRIDE;

private slots:
    void startRecording();
    void stopRecording();

private:
    Ui::MainWindow *ui;
    QWidget *centralWidget;
    QVBoxLayout* mainLayout;
    cameraWidget* camera;
    void createContextMenu();

    QAction* startRec;
    QAction* stopRec;
};

#endif // MAINWINDOW_H
