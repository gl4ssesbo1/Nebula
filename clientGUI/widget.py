# coding=utf-8
# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import json
import requests

from MainNebulaWindow import MainNebulaWindow

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QSystemTrayIcon)
from PyQt5 import QtWidgets, uic, QtGui
from PySide2.QtWidgets import QApplication, QWidget #QDesigner
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
#from PySide2.QtGui import *

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        #self.load_ui()
        uic.loadUi("form.ui", self)
        #self.setWindowIcon(QtGui.QIcon('logo.png'))

        title = "Nebula Client"
        self.setWindowTitle(title)

        self.show()

        self.loginButton.clicked.connect(self.login)

    def login(self):
        username = self.loginlineEdit.text()
        password = self.passwordlineEdit.text()
        workspace = self.workspacelineEdit.text()
        apihost = self.apiHostlineEdit.text()

        try:
            apiport = int(self.apiPortlineEdit.text())
        except ValueError:
            msg = QMessageBox()
            msg.setText("Port should be an integer")
            msg.exec_()
            del(msg)

        password = self.passwordlineEdit.text()

        try:
            jwt_token_dict = json.loads(requests.post("http://{}:{}/api/latest/cosmonauts".format(apihost, str(apiport)), json={"cosmonaut_name": username, "cosmonaut_pass": password}).text)
            if 'token' in jwt_token_dict:
                jwt_token = jwt_token_dict['token']
                self.hide()
                mainwindow.getTeamServerInfo(apihost, apiport, jwt_token, workspace, username)
                mainwindow.show()

            else:
                msg = QMessageBox()
                msg.setText("{}".format(jwt_token_dict['error']))
                msg.exec_()
                del(msg)

        except requests.exceptions.ConnectionError:
            msg = QMessageBox()
            msg.setText("Failed to establish a new connection to the Teamserver API Server")
            msg.exec_()
            del(msg)

        except:
            msg = QMessageBox()
            msg.setText("{}".format(sys.exc_info()[1]))
            msg.exec_()
            del(msg)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    trayIcon = QSystemTrayIcon(QtGui.QIcon('logo.png'), parent=app)
    trayIcon.setToolTip("Nebula")
    trayIcon.show()

    mainwindow = MainNebulaWindow()
    widget = Widget()

    #app.exec_()

    #widget.show()
    sys.exit(app.exec_())
