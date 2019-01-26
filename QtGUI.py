# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QtGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.createRobotButton = QtWidgets.QPushButton(self.centralwidget)
        self.createRobotButton.setGeometry(QtCore.QRect(810, 80, 171, 31))
        self.createRobotButton.setObjectName("createRobotButton")
        self.createObstacleButton = QtWidgets.QPushButton(self.centralwidget)
        self.createObstacleButton.setEnabled(True)
        self.createObstacleButton.setGeometry(QtCore.QRect(810, 120, 171, 31))
        self.createObstacleButton.setObjectName("createObstacleButton")
        self.minsowskiButton = QtWidgets.QPushButton(self.centralwidget)
        self.minsowskiButton.setGeometry(QtCore.QRect(890, 365, 91, 31))
        self.minsowskiButton.setObjectName("minsowskiButton")
        self.moveRobotButton = QtWidgets.QPushButton(self.centralwidget)
        self.moveRobotButton.setGeometry(QtCore.QRect(810, 300, 171, 31))
        self.moveRobotButton.setObjectName("moveRobotButton")
        self.findPathMode = QtWidgets.QPushButton(self.centralwidget)
        self.findPathMode.setGeometry(QtCore.QRect(810, 470, 171, 31))
        self.findPathMode.setObjectName("findPathMode")
        self.showMapButton = QtWidgets.QPushButton(self.centralwidget)
        self.showMapButton.setGeometry(QtCore.QRect(810, 420, 171, 31))
        self.showMapButton.setObjectName("showMapButton")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(810, 230, 171, 31))
        self.loadButton.setObjectName("loadButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(810, 190, 171, 31))
        self.saveButton.setObjectName("saveButton")
        self.logArea = QtWidgets.QTextBrowser(self.centralwidget)
        self.logArea.setGeometry(QtCore.QRect(810, 520, 171, 251))
        self.logArea.setObjectName("logArea")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(810, 370, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.createRobotButton.setText(_translate("MainWindow", "Create robot"))
        self.createObstacleButton.setText(_translate("MainWindow", "Create obstacle"))
        self.minsowskiButton.setText(_translate("MainWindow", "Normal"))
        self.moveRobotButton.setText(_translate("MainWindow", "Drag robot"))
        self.findPathMode.setText(_translate("MainWindow", "Enable path finding"))
        self.showMapButton.setText(_translate("MainWindow", "Show map"))
        self.loadButton.setText(_translate("MainWindow", "Load"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.label.setText(_translate("MainWindow", "Display type:"))

