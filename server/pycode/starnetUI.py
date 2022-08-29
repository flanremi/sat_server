# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'starnet.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from main import *


def showMovie(url, start, end):
    from myVlc.play import Player
    time.sleep(int(start) / 10)
    player = Player()
    player.play(url)
    time.sleep((int(end) - int(start)) / 10)
    player.stop()

def observation(lat, lon, dur):
    log("开始协同观测")
    import _thread
    from time_varying.TimeVarying import getResult
    play_queue = getResult(lat, lon, dur)
    log(str(play_queue))
    for p in play_queue:
        _thread.start_new_thread(showMovie, (p.get("url"), p.get("start"), p.get('end')))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 20, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(550, 40, 89, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 90, 751, 461))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 60, 67, 17))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 20, 89, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(470, 0, 50, 31))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(400, 10, 67, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(400, 40, 67, 17))
        self.label_3.setObjectName("label_3")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(470, 30, 50, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(470, 60, 50, 31))
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(400, 70, 67, 17))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "StarNet"))
        self.pushButton.setText(_translate("MainWindow", "任务迁移"))
        self.pushButton_2.setText(_translate("MainWindow", "协同观测"))
        self.pushButton_3.setText(_translate("MainWindow", "清除任务"))
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText(_translate("MainWindow", "日志信息"))
        self.label_2.setText(_translate("MainWindow", "用户纬度"))
        self.label_3.setText(_translate("MainWindow", "用户经度"))
        self.label_4.setText(_translate("MainWindow", "服务时长"))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.onClick_Button())
        self.ui.pushButton_2.clicked.connect(lambda: self.onClick_Button())
        self.ui.pushButton_3.clicked.connect(lambda: self.onClick_Button())
        bindScreen(self)

    def onClick_Button(self):
        sender = self.sender()
        if sender == self.ui.pushButton:
            yolo()
        elif sender == self.ui.pushButton_3:
            deleteAllDeploy()
        elif sender == self.ui.pushButton_2:
            observation(self.ui.textEdit.toPlainText(),
                        self.ui.textEdit_2.toPlainText(),
                        self.ui.textEdit_3.toPlainText(),
                        )

    def logNotify(self):
        self.ui.textBrowser.setText(getLog())
        self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
