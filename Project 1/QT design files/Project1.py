# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Project1.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 50, 131, 41))
        self.label.setObjectName("label")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(280, 50, 221, 41))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(530, 50, 129, 38))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(530, 170, 151, 38))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(130, 170, 91, 41))
        self.label_3.setObjectName("label_3")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(280, 170, 221, 41))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_4 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_4.setGeometry(QtCore.QRect(280, 110, 221, 41))
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.graphicsView_5 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_5.setGeometry(QtCore.QRect(280, 230, 221, 41))
        self.graphicsView_5.setObjectName("graphicsView_5")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 110, 221, 41))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 230, 251, 41))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 34))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Temperature"))
        self.pushButton.setText(_translate("MainWindow", "Get Temp"))
        self.pushButton_3.setText(_translate("MainWindow", "Get Humidity"))
        self.label_3.setText(_translate("MainWindow", "Humidity"))
        self.label_4.setText(_translate("MainWindow", "Temp Time of Request"))
        self.label_5.setText(_translate("MainWindow", "Humidity Time of Request"))

