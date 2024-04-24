# coding=utf-8
# This Python file uses the following encoding: utf-8

# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from datetime import datetime
import platform
import json
import requests
import flask_mongoengine
import random

#from colorama import colored

from AddCredentials import AddCredentials
from FilterGraphListWidget import FilterGraphListWidget

from PyQt5.QtWidgets import (QGraphicsLineItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsTextItem, QFrame, QFormLayout, QGroupBox, QSpacerItem, QVBoxLayout, QLayout, QMenu, QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QSizePolicy, QGraphicsScene, QGraphicsView, QGraphicsItem)
from PyQt5 import QtWidgets, uic, QtGui, QtCore

from PyQt5 import QtGui

from PyQt5.QtGui import *
from PySide2.QtWidgets import QApplication, QWidget #QDesigner
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
#from PySide2.QtGui import *

from PyQt5.QtCore import Qt, QSize

#global initial_console_string

#global current_module
system = platform.system()

class MainNebulaWindow(QtWidgets.QMainWindow):

    # ---------------------------------------
    # Graph View
    # ---------------------------------------
    domains = []
    domain = {}

    awsusers = []
    awsuser = {}

    # ---------------------------------------

    initial_console_string = "({})()({}) >>> "
    current_module = "Nebula"
    apiHost = ""
    apiPort = 0
    token = ""
    workspace = ""
    username = ""

    moduleVerticalLayout = None
    #group_box = None
    groupBox = None
    formLayout = None

    #groupBox = QGroupBox()

    objectsGraphicScene = None

    redBrush = QBrush(Qt.red)
    blueBrush = QBrush(Qt.blue)
    greenBrush = QBrush(Qt.green)
    yellowBrush = QBrush(Qt.yellow)
    purpleBrush = QBrush(Qt.magenta)
    #greyBrush = QBrush(Qt.grey)
    blackBrush = QBrush(Qt.black)

    blackPen = QPen(Qt.black)
    blackPen.setWidth(4)

    module_options = {}

    filtered_modules = []

    moduleOptionrGidBoxes = {}
    cred_prof = ""

    moduleNeedsCreds = False

    dynamically_generated_options = {}

    useragent = ""

    useragents = [
        'Boto3/1.7.48 Python/3.9.1 Windows/10 Botocore/1.10.48',
        'Boto3/1.7.48 Python/3.8.1 Windows/10 Botocore/1.10.48',
        'Boto3/1.7.48 Python/2.7.0 Windows/10 Botocore/1.10.48',
        'Boto3/1.7.48 Python/3.9.1 Windows/8 Botocore/1.10.48',
        'Boto3/1.7.48 Python/3.8.1 Windows/8 Botocore/1.10.48',
        'Boto3/1.7.48 Python/2.7.0 Windows/8 Botocore/1.10.48',
        'Boto3/1.7.48 Python/3.9.1 Windows/7 Botocore/1.10.48',
        'Boto3/1.7.48 Python/3.8.1 Windows/7 Botocore/1.10.48',
        'Boto3/1.7.48 Python/2.7.0 Windows/7 Botocore/1.10.48',
        'Boto3/1.9.89 Python/2.7.12 Linux/4.1.2-34-generic',
        'Boto3/1.9.89 Python/3.8.1 Linux/4.1.2-34-generic',
        'Boto3/1.9.89 Python/3.9.1 Linux/5.9.0-34-generic'
    ]

    all_sessions = []
    allmodules = []

    module_type = [
        'cleanup',
        'detection',
        'detectionbypass',
        'enum',
        'exploit',
        'lateralmovement',
        'listeners',
        'persistence',
        'privesc',
        'reconnaissance',
        'stager',
        'misc'
    ]

    nr_of_modules = {
        'cleanup': "",
        'detection': "",
        'detectionbypass': "",
        'enum': "",
        'exploit': "",
        'lateralmovement': "",
        'listeners': "",
        'persistence': "",
        'privesc': "",
        'reconnaissance': "",
        'stager': "",
        'misc': ""
    }

    nr_of_cloud_modules = {
        "aws": 0,
        "gcp": 0,
        "azure": 0,
        "office365": 0,
        "docker": 0,
        "kube": 0,
        "misc": 0,
        "azuread": 0,
        "digitalocean": 0
    }

    clouds = [
        "aws",
        "gcp",
        "azure",
        "office365",
        "docker",
        "kube",
        "azuread",
        "misc",
        #"digitalocean"
    ]

    def __init__(self):
        super(MainNebulaWindow, self).__init__()
        #self.load_ui()
        uic.loadUi("mainwindow.ui", self)

        title = "Nebula Client"
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle(title)

        self.fillModuleComboBox()

        self.moduleVerticalLayout = QVBoxLayout()
        self.groupBox = QGroupBox()
        self.formLayout = QFormLayout()

        self.objectsGraphicScene = QGraphicsScene()
        self.graphGraphicsView.setScene(self.objectsGraphicScene)

        self.moduleParentFrame.setStyleSheet('background-color: white')
        self.cosmonautsListWidget.setStyleSheet('background-color: white')
        #self.moduleChildFrame.setStyleSheet('background-color: rgb(240, 240, 240)')
        self.logsFrame.setStyleSheet('background-color: white')

        self.nebulaConsoleTextEdit.setStyleSheet('background-color: black')
        greenColor = QColor(50, 209, 16)
        self.nebulaConsoleTextEdit.setTextColor(greenColor)

        self.particleConsoleTextEdit.setStyleSheet('background-color: black')
        self.particleConsoleTextEdit.setTextColor(greenColor)

        self.commandLineEdit.returnPressed.connect(self.runCommandButton.click)
        #self.particleCommandLineEdit.returnPressed.connect(self.runCommandButton.click)

        self.logsTextEdit.setStyleSheet('background-color: black')
        self.logsTextEdit.setTextColor(greenColor)

        self.modulesComboBox.setPlaceholderText("Modules");
        self.modulesComboBox.setCurrentIndex(-1)

        self.typeOfListenerCombobox.setPlaceholderText("Type of Listener");
        self.typeOfListenerCombobox.setCurrentIndex(-1)
        self.credsListWidget.itemSelectionChanged.connect(self.fillCredTextEdit)
        self.moduleListWidget.itemSelectionChanged.connect(self.useModule)
        self.runModulePushButton.clicked.connect(self.runModule)
        self.credsToUseComboBox.activated.connect(self.setCredentials)
        self.userAgentComboBox.activated.connect(self.setUserAgent)

        self.setUserAgentPushButton.clicked.connect(self.setUserAgentTextEdit)
        self.addCredPushButton.clicked.connect(self.addCredentialsFunction)

        self.modulesComboBox.activated.connect(self.filterModulesVendor)
        self.modulesTypeComboBox.activated.connect(self.filterModuleType)

        self.removeCredPushButton.clicked.connect(self.removeCredPushButtonFunction)

        self.commandHistoryComboBox.activated.connect(self.addCommandFromHistory)

        self.resetCosmonautPasswordPushButton.clicked.connect(self.resetCosmonautPasswrod)

        self.fillFilterGraphListWidget()
        self.filterGraphListWidget.itemSelectionChanged.connect(self.selectTheFilter)


        #self.listAllSubDomains()

    def setCredentials(self):
        self.cred_prof = str(self.credsToUseComboBox.currentText())

    def addCredentialsFunction(self):
        addcredentials = AddCredentials(self.token, self.apiHost, self.apiPort, self.workspace)
        #addcredentials.show()
        addcredentials.exec_()

        #addcredentials.setTeamserverSettings(self.token, self.apiHost, self.apiPort, self.workspace)

        self.credsListWidget.clear()
        self.credsTextEdit.clear()

        self.fillCredentials()

        #del(addcredentials)

    def removeCredPushButtonFunction(self):
        self.all_sessions.clear()
        awscred = self.credsListWidget.currentItem().text()
        body = {
            "aws_profile_name": awscred
        }

        run_module_output = requests.delete("http://{}:{}/api/latest/awscredentials".format(self.apiHost, self.apiPort),
                                                                        json=body,
                                                                        headers={"Authorization": "Bearer {}".format(
                                                                           self.token)})

        run_module_json = json.loads(run_module_output.text)

        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('logo.png'))

        if run_module_output.status_code == 200:
            msg.setWindowTitle("Successful")
            msg.setText(
                run_module_json['message']
            )
        else:
            msg.setWindowTitle("Error")
            msg.setText(
                run_module_json['error']
            )

        msg.exec_()
        del(msg)

        self.credsListWidget.clear()
        self.credsTextEdit.clear()

        self.fillCredentials()

    def generateElements(self):
        print()

    def getTeamServerInfo(self, apiHost, apiPort, token, workspace, username):
        self.apiHost = apiHost
        self.apiPort = apiPort
        self.token = token
        self.workspace = workspace
        self.username = username
        self.logsTextEdit.insertPlainText("[{}] User {} Logged in\n".format(datetime.now(), self.username))
        self.nebulaConsoleTextEdit.insertPlainText(self.initial_console_string.format(self.workspace, self.current_module))

        self.fillCredentials()
        self.fillModuleListWidget()
        self.fillCosmonautTextEdit()

        self.listAllDomains(self.apiHost, self.apiPort,  self.token)

    def clearLayout(self, layout):
        for i in range(layout.count()+100):
            try:
                layout.itemAt(i).widget().deleteLater()
            except:
                pass

    def runModule(self):
        if self.current_module == 'Nebula':
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('logo.png'))
            msg.setWindowTitle("Error")
            msg.setText("Select a module first.")
            msg.exec_()
            del(msg)
            return False
        else:
            if self.moduleNeedsCreds and self.cred_prof == "":
                msg = QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('logo.png'))
                msg.setWindowTitle("Error")
                msg.setText("Select a credential please.")
                msg.exec_()
                del(msg)
                return False
            else:
                for c,v in self.dynamically_generated_options.items():
                    if c == 'SERVICE':
                        self.module_options[c]['value'] = v['value']
                    else:
                        if v['required'] == 'true' and (v["lineedit"]).text() == "":
                            msg = QMessageBox()
                            msg.setWindowIcon(QtGui.QIcon('logo.png'))
                            msg.setWindowTitle("Error")
                            msg.setText("Option '{}' is required.".format(c))
                            msg.exec_()
                            del(msg)
                            return False
                        else:
                            #qLineEdit = group_box.findChild(QLineEdit).text()
                            qLineEdit = (v["lineedit"]).text()
                            self.module_options[c]['value'] = qLineEdit

                self.logsTextEdit.insertPlainText("[{}] User {} ran module {}\n".format(datetime.now(), self.username, self.current_module))
                run_module_options ={
                        'module': self.current_module,
                        'module_options': self.module_options,
                        'cred-prof': self.cred_prof,
                        'user-agent': self.useragent,
                        'workspace': self.workspace
                }

                run_module_output = requests.post("http://{}:{}/api/latest/modules/run".format(self.apiHost, self.apiPort),
                                                                                json=run_module_options,
                                                                                headers={"Authorization": "Bearer {}".format(
                                                                                   self.token)}).text

                run_module_json = json.loads(run_module_output)
                if "error" in run_module_json:
                    self.logsTextEdit.insertPlainText("[{}] Module {} error: {}\n".format(datetime.now(), self.current_module ,run_module_json['error']))
                    self.nebulaConsoleTextEdit.insertPlainText("{}\n".format(run_module_json['error']))
                    self.nebulaConsoleTextEdit.insertPlainText(self.initial_console_string.format(self.workspace, self.current_module))
                    return False
                else:
                    self.nebulaConsoleTextEdit.insertPlainText("use module {}\n".format(
                                        self.current_module
                                        )
                                    )

                    for key, value in (run_module_options['module_options']).items():
                        if key == "SERVICE":
                            pass
                        else:
                            self.nebulaConsoleTextEdit.insertPlainText(self.initial_console_string.format(self.workspace, self.current_module))
                            self.nebulaConsoleTextEdit.insertPlainText("set {} {}\n".format(key, value['value']))

                    self.nebulaConsoleTextEdit.insertPlainText(self.initial_console_string.format(self.workspace, self.current_module))
                    self.nebulaConsoleTextEdit.insertPlainText("run\n")
                    self.logsTextEdit.insertPlainText("[{}] Module {} ran successfully\n".format(datetime.now(), self.current_module))
                    self.nebulaConsoleTextEdit.insertPlainText("{}\n".format(json.dumps(run_module_json, indent=4, default=str)))
                    self.nebulaConsoleTextEdit.insertPlainText(self.initial_console_string.format(self.workspace, self.current_module))
                    del(run_module_json)

    def fillCosmonautTextEdit(self):
        user_listed = json.loads(requests.get("http://{}:{}/api/latest/cosmonauts".format(self.apiHost, self.apiPort),
                                                                      headers={
                                                                          "Authorization": "Bearer {}".format(self.token)}).text)

        if not "error" in user_listed:
            for cosmonaut in user_listed['cosmonauts']:
                self.cosmonautsListWidget.addItem(cosmonaut)

        else:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('logo.png'))
            msg.setWindowTitle("Error")
            msg.setText("{}".format(user_listed['error']))
            msg.exec_()
            del(msg)

    def resetCosmonautPasswrod(self):
        user_passwod = self.cosmonautPasswordLineEdit.text()
        user_passwodconfirm = self.cosmonautPasswordConfirmLineEdit.text()
        cosmonaut_name = self.cosmonautsListWidget.currentItem().text()

        if user_passwod == "" or user_passwodconfirm == "":
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.self.QIcon('logo.png'))
            msg.setWindowTitle("Error")
            msg.setText("Password can't be empty")
            msg.exec_()
            del(msg)

        else:
            if not user_passwod == user_passwodconfirm:
                msg = QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('logo.png'))
                msg.setWindowTitle("Error")
                msg.setText("Passwords are not the same")
                msg.exec_()
                del(msg)
            else:
                user_json = {
                    "cosmonaut_name": cosmonaut_name,
                    "cosmonaut_pass": user_passwod
                }
                user_created = json.loads(requests.patch("http://{}:{}/api/latest/cosmonauts".format(self.apiHost, self.apiPort),
                                                       json=user_json,
                                                       headers={"Authorization": "Bearer {}".format(
                                                           self.token)}).text)
                del user_json
                if not "error" in user_created:
                    msg = QMessageBox()
                    msg.setWindowIcon(QtGui.QIcon('logo.png'))
                    msg.setWindowTitle("Successful")
                    msg.setText("User '{}' Password's reseted.".format(cosmonaut_name))
                    msg.exec_()
                    del(msg)
                else:

                    msg = QMessageBox()
                    msg.setWindowIcon(QtGui.QIcon('logo.png'))
                    msg.setWindowTitle("Error")
                    msg.setText(user_created['error'])
                    msg.exec_()
                    del(msg)

    def useModule(self):
        self.dynamically_generated_options.clear()
        #self.clearLayout(self.moduleOptionsScrollArea)
        #self.formLayout = QFormLayout()
        self.clearLayout(self.formLayout)
        module_options = json.loads(requests.post("http://{}:{}/api/latest/modules/use".format(self.apiHost, self.apiPort), json={"module": self.moduleListWidget.currentItem().text()}, headers = {"Authorization": "Bearer {}".format(self.token)}).text)

        #scroll = QScrollableArea()
        #self.moduleOptionsScrollArea.setWidget(self.optionsVerticalLayout.widget())
        self.moduleOptionsScrollArea.setWidgetResizable(True)
        #self.moduleOptionsScrollArea.setFixedHeight(260)

        self.moduleOptionsScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.moduleOptionsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if not "error" in module_options:
            self.current_module = module_options['module_name']
            self.currentModuleLabel.setText(self.current_module)

            self.consoleCommandLabel.setText(module_options['cli_comm'])
            self.needsCredsLabel.setText(str(module_options['needs_creds']))
            self.moduleNeedsCreds = module_options['needs_creds']
            self.descriptionLabel.setText(module_options['description'])

            if not module_options['needs_creds']:
                self.credsToUseComboBox.setEnabled(False)
            else:
                self.credsToUseComboBox.setEnabled(True)
            self.module_options = module_options["module_options"]

            for c, v in (module_options["module_options"]).items():
                if c == 'SERVICE':
                    #group_box = QtWidgets.QGroupBox()
                    self.serviceLabel.setText(v['value'])
                    #self.dynamically_generated_options[c]['value'] = v['value']
                    self.dynamically_generated_options[c] = {
                        "lineedit": None,
                        "required": v['required'],
                        "value": v['value']
                    }
                else:
                    self.create(c, v)


            author = ""
            for x, y in module_options['author'].items():
                author += ("{}: {}\n".format(x, y))



            self.authorLabel.setText(author)


            self.groupBox.setLayout(self.formLayout)

            self.moduleOptionsScrollArea.setWidget(self.groupBox)
            self.moduleOptionsScrollArea.setWidgetResizable(True)
            self.moduleOptionsScrollArea.setFixedHeight(240)

            self.moduleVerticalLayout.addWidget(self.moduleOptionsScrollArea)

        else:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('logo.png'))
            msg.setWindowTitle("Error")
            msg.setText("{}".format(user_listed['error']))
            msg.exec_()
            del(msg)

    def create(self, c, v):
        serial_label = None
        serial_lineedit = None
        if v['required'] == "true":
            cwild = c + "*"
            serial_label = QtWidgets.QLabel(cwild)

        else:
            serial_label = QtWidgets.QLabel(c)

        serial_label.setToolTip(v['description'])


        if 'wordlist' in v:
            serial_lineedit = QtWidgets.QTextEdit(v['value'])

        else:
            serial_lineedit = QtWidgets.QLineEdit(v['value'])

        isrequired = v['required']

        self.dynamically_generated_options[c] = {
            "lineedit": serial_lineedit,
            "required": v['required'],
            "value": ""
        }

        self.formLayout.addRow(serial_label, serial_lineedit)

    def filterModulesVendor(self):
        self.moduleListWidget.clear()
        self.filtered_modules = self.allmodules
        moduletype = str(self.modulesComboBox.currentText())

        if moduletype == 'All':
            for mdl in self.filtered_modules:
                self.moduleListWidget.addItem(mdl)

        else:
            if len(self.filtered_modules) == 0:
                pass
            else:
                for mdl in self.filtered_modules:
                    mvendor = ((mdl.split("/")[1]).split("_")[0])

                    if moduletype == mvendor:
                        self.moduleListWidget.addItem(mdl)
                    else:
                        pass
                        #self.filtered_modules.remove(mdl)
                    del(mvendor)

    def filterModuleType(self):
        self.moduleListWidget.clear()
        moduletype = str(self.modulesTypeComboBox.currentText())

        if self.modulesComboBox.currentText() == None:
            for mdl in self.allmodules:
                self.moduleListWidget.addItem(mdl)

        else:
            if moduletype == "All":
                modulevendor = str(self.modulesComboBox.currentText())

                for mdl in self.filtered_modules:
                    mvendor = ((mdl.split("/")[1]).split("_")[0])

                    if modulevendor == mvendor:
                        self.moduleListWidget.addItem(mdl)
                    else:
                        pass
                        #self.filtered_modules.remove(mdl)
                    del(mvendor)
            else:
                modulevendor = str(self.modulesComboBox.currentText())

                for mdl in self.filtered_modules:
                    mvendor = ((mdl.split("/")[1]).split("_")[0])

                    if modulevendor == mvendor and moduletype == (mdl.split("/")[0]):
                        self.moduleListWidget.addItem(mdl)
                    else:
                        pass
                        #self.filtered_modules.remove(mdl)
                    del(mvendor)



    def fillModuleListWidget(self):
        modules_json = json.loads(requests.get("http://{}:{}/api/latest/modules".format(self.apiHost, self.apiPort), headers = {"Authorization": "Bearer {}".format(self.token)}).text)['modules']

        for m in modules_json:
            if "digitalocean" in m['amodule']:
                pass
            else:
                self.allmodules.append(m['amodule'])
                self.moduleListWidget.addItem(m['amodule'])
                self.filtered_modules.append(m['amodule'])

    def setUserAgent(self):
        self.useragent = str(self.userAgentComboBox.currentText())
        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('logo.png'))
        msg.setWindowTitle("Error")
        msg.setText(self.useragent)
        msg.exec_()
        del(msg)

    def setUserAgentTextEdit(self):
        self.useragent = str(self.userAgentTextEdit.toPlainText())
        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon('logo.png'))
        msg.setWindowTitle("Error")
        msg.setText(self.useragent)
        msg.exec_()
        del(msg)

    def fillModuleComboBox(self):
        self.modulesComboBox.addItem("All")
        for cloud in self.clouds:
            self.modulesComboBox.addItem(cloud)

        for ua in self.useragents:
            self.userAgentComboBox.addItem(ua)

        self.modulesTypeComboBox.addItem("All")
        for mtype in self.module_type:
            self.modulesTypeComboBox.addItem(mtype)

    def fillCredTextEdit(self):
        self.credsTextEdit.clear()
        for creds in self.all_sessions:
            if creds['profile'] == self.credsListWidget.currentItem().text():
                self.credsTextEdit.append("-------------------------------------")

                self.credsTextEdit.append("{}: {}".format(
                    "Profile",
                    creds['profile']
                ))
                self.credsTextEdit.append("-------------------------------------")
                for key, value in creds.items():
                    self.credsTextEdit.append("{}: {}".format(key, value))

    def fillCredentials(self):
        self.all_sessions.clear()

        self.credsToUseComboBox.clear()

        aws_sessions = json.loads(requests.get("http://{}:{}/api/latest/awscredentials".format(self.apiHost, self.apiPort),
                                               headers={"Authorization": "Bearer {}".format(self.token)}).text)

        azure_sessions = json.loads(requests.get("http://{}:{}/api/latest/azurecredentials".format(self.apiHost, self.apiPort),
                                               headers={"Authorization": "Bearer {}".format(self.token)}).text)

        digitalocean_sessions = json.loads(requests.get("http://{}:{}/api/latest/digitaloceancredentials".format(self.apiHost, self.apiPort),
                                              headers={"Authorization": "Bearer {}".format(self.token)}).text)

        for do_sess in digitalocean_sessions:
            if "digitalocean_token" in do_sess:
                self.all_sessions.append(
                    {
                        'provider': 'DIGITALOCEAN',
                        'profile': do_sess['digitalocean_profile_name'],
                        'digitalocean_token': do_sess['digitalocean_token'],
                    }
                )
            else:
                if not 'digitalocean_region' in do_sess:
                    do_sess['digitalocean_region'] = ""

                self.all_sessions.append(
                    {
                        'provider': 'DIGITALOCEAN',
                        'profile': do_sess['digitalocean_profile_name'],
                        'access_key_id': do_sess['digitalocean_access_key'],
                        'secret_key': do_sess['digitalocean_secret_key'],
                        'region': do_sess['digitalocean_region']
                    }
                )

        for aws_sess in aws_sessions:
            if "aws_session_token" in aws_sess:
                self.all_sessions.append(
                    {
                        'provider': 'AWS',
                        'profile': aws_sess['aws_profile_name'],
                        'access_key_id': aws_sess['aws_access_key'],
                        'secret_key': aws_sess['aws_secret_key'],
                        'session_token': aws_sess['aws_session_token'],
                        'region': aws_sess['aws_region']
                    }
                )
            else:
                if not 'aws_region' in aws_sess:
                    aws_sess['aws_region'] = ""


                self.all_sessions.append(
                    {
                        'provider': 'AWS',
                        'profile': aws_sess['aws_profile_name'],
                        'access_key_id': aws_sess['aws_access_key'],
                        'secret_key': aws_sess['aws_secret_key'],
                        'region': aws_sess['aws_region']
                    }
                )
        for creds in self.all_sessions:
            self.credsToUseComboBox.addItem(creds['profile'])
            self.credsListWidget.addItem(creds['profile'])

    def addCommandFromHistory(self):
        self.commandLineEdit.setText(str(self.commandHistoryComboBox.currentText()))

    @QtCore.pyqtSlot()
    def on_runCommandButton_clicked(self):
        command = self.commandLineEdit.text()

        self.logsTextEdit.insertPlainText("[{}] User {} ran command: {}\n".format(datetime.now(), self.username, command))
        self.commandLineEdit.clear()

        self.nebulaConsoleTextEdit.insertPlainText("{}\n".format(command))

        self.commandHistoryComboBox.addItem(command)
        count = self.commandHistoryComboBox.count()
        self.commandHistoryComboBox.setCurrentIndex(count-1)

        if command == "use":
            self.nebulaConsoleTextEdit.insertPlainText("{}\n".format(command))
            self.nebulaConsoleTextEdit.insertPlainText(self.initial_console_string.format(self.workspace, self.current_module))
        else:
            try:
                if system == 'Windows':
                    cmd = "powershell.exe " + command
                    out = os.popen(cmd).read()
                    self.nebulaConsoleTextEdit.insertPlainText("{}\n".format(out))

                elif system == 'Linux' or system == 'Darwin':
                    out = os.popen(command).read()
                    self.nebulaConsoleTextEdit.insertPlainText("{}\n".format(out))

            except:
                self.nebulaConsoleTextEdit.insertPlainText("'{}' is not a valid command.\n".format(command))

        self.nebulaConsoleTextEdit.insertPlainText(self.initial_console_string.format(self.workspace, self.current_module))

    def listAllDomains(self, apihost, apiport,  jwt_token):
        try:
            domains = json.loads(requests.get("http://{}:{}/api/latest/domains".format(apihost, apiport), headers={"Authorization": "Bearer {}".format(jwt_token)}).text)
            self.domains = domains
            return True
        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('logo.png'))
            msg.setWindowTitle("Error")
            msg.setText(str(sys.exc_info()))
            msg.exec_()
            del(msg)

            return False

    def listAllSubdomainsForDomain(self, apihost, apiport, domain, jwt_token):
        try:
            domain_dict = json.loads(requests.post("http://{}:{}/api/latest/domains".format(apihost, apiport), json={"dn_name": domain}, headers={"Authorization": "Bearer {}".format(jwt_token)}).text)
            self.domain = domain_dict['dn_name']

            return True

        except flask_mongoengine.DoesNotExist:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('logo.png'))
            msg.setWindowTitle("Error")
            msg.setText("Domain does not exist")
            msg.exec_()
            del(msg)

            return False

        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('logo.png'))
            msg.setWindowTitle("Error")
            msg.setText(str(sys.exc_info()))
            msg.exec_()
            del(msg)

            return False

    # -------------------------------------------------
    #       Graph View
    # -------------------------------------------------

    def fillFilterGraphListWidget(self):
        commands = [
            "AWS",
            "List All Users",
            "    List All User's Groups",
            "    List All User's Policies",
            "    List All User's Credentials",
            "List All Groups",
            "    List All Group's User",
            "    List All Group's Policies",
            "List All Instances",
            "List All Policies",
            "List User Policies",
            "Misc",
            "List Domain and it's subdomains"
        ]
        for command in commands:
            self.filterGraphListWidget.addItem(command)

        for i in range(0, len(self.filterGraphListWidget)):
            if self.filterGraphListWidget.item(i).text() == "AWS" or self.filterGraphListWidget.item(i).text() == "Misc":
                self.filterGraphListWidget.item(i).setBackground(QColor(206,206,206))
                self.filterGraphListWidget.item(i).setFlags(Qt.NoItemFlags)

    def selectTheFilter(self):
        self.objectsGraphicScene.clear()

        if self.filterGraphListWidget.currentItem().text() == "List Domain and it's subdomains":
            self.listAllSubDomains()

        elif self.filterGraphListWidget.currentItem().text() == "List All Users":
            self.awsUsersGraphView()

        elif self.filterGraphListWidget.currentItem().text().replace("    ", "") == "List All User's Groups":
            self.getAWSUserGroups()

        elif self.filterGraphListWidget.currentItem().text().replace("    ", "") == "List All User's Policies":
            self.getAWSUserPolicies()

    def getAWSUsersInfo(self):
        if self.listAllAWSUsers():
            filterGraphListWidget = FilterGraphListWidget()

            user_names = []
            for dn in self.awsusers:
                user_names.append(dn['aws_username'])

            filterGraphListWidget.fillFilterGraphListWidget(user_names)
            filterGraphListWidget.exec_()

            if filterGraphListWidget.target == None or filterGraphListWidget.target == "" :
                return None

            user = filterGraphListWidget.target
            return user

    def getAWSUserPolicies(self):
        rects = []
        policies = []

        user = self.getAWSUsersInfo()
        if user == None:
            return

        for username in self.awsusers:
            rects = []

            if username['aws_username'] == user:
                for gpolicy in username['aws_group_policies']:
                    policies.append("Group Policy: {}".format(gpolicy))

                for gapolicy in username['aws_group_attached_policies']:
                    policies.append("Group Attached Policy: {}".format(gapolicy))

                for uappolicy in username['aws_user_attached_policies']:
                    policies.append("User Attached Policy: {}".format(uappolicy['PolicyName']))

                for umppolicy in username['aws_user_managed_attached_policies']:
                    policies.append("User Managed Policy: {}".format(umppolicy))

                for uppolicy in username['aws_user_policies']:
                    policies.append("User Policy: {}".format(uppolicy))

                rectWidth = len(user) * 10
                rectHeight = 50
                userY = 0
                userX = (len(username['aws_user_groups']) * 200)/2

                user_rect = self.drawRect(userX, userY, rectWidth, rectHeight, user, QColor(192, 192, 192), False)

                rectY = (len(policies) * 200)/2
                for policy in policies:
                    rectWidth = len(policy) * 10
                    rectX = 0

                    subdomainrect = self.drawRect(rectX, rectY, rectWidth, rectHeight, policy, QColor(0, 162, 232), False)

                    self.createLineItem(user_rect, subdomainrect, userX, userY, rectX, rectY)
                    rectY = -60

                break

    def getAWSUserGroups(self):
        rects = []
        usernames = []

        user = self.getAWSUsersInfo()

        for username in self.awsusers:
            rects = []

            if username['aws_username'] == user:
                rectWidth = len(user) * 10
                rectHeight = 50
                userY = 0
                userX = (len(username['aws_user_groups']) * 200)/2

                user_rect = self.drawRect(userX, userY, rectWidth, rectHeight, user, QColor(192, 192, 192), False)

                rectY = (len(username['aws_user_groups']) * 200)/2
                for group in username['aws_user_groups']:
                    rectWidth = len(group) * 10
                    rectX = 0

                    subdomainrect = self.drawRect(rectX, rectY, rectWidth, rectHeight, group, QColor(0, 162, 232), False)

                    self.createLineItem(user_rect, subdomainrect, userX, userY, rectX, rectY)
                    rectY = -60

                break

    def awsUsersGraphView(self):
        status = self.listAllAWSUsers()

        if status:
            rects = []
            usernames = []

            for user in self.awsusers:
                usernames.append(user['aws_username'])

            for username in usernames:
                rectWidth = len(username) * 10
                rectHeight = 50
                rectX = random.randrange(0,1000)
                rectY = random.randrange(0,1000)
                subdomainrect = self.drawRect(rectX, rectY, rectWidth, rectHeight, username, QColor(0, 162, 232), True)
                #rects.append(subdomainrect)

                #self.createLineItem(domain_rect, subdomainrect, domainX, domainY, rectX, rectY)

    def listAllAWSUsers(self):
        try:
            user_dict = json.loads(requests.get("http://{}:{}/api/latest/awsusers".format(self.apiHost, self.apiPort), headers={"Authorization": "Bearer {}".format(self.token)}).text)

            self.awsusers = user_dict
            #for key, value in user_dict.items():
            #    self.awsusers.append()

            return True

        except:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('logo.png'))
            msg.setWindowTitle("Error")
            msg.setText(str(sys.exc_info()))
            msg.exec_()
            del(msg)

            return False

    def listAllSubDomains(self):
        filterGraphListWidget = FilterGraphListWidget()

        if self.listAllDomains(self.apiHost, self.apiPort,  self.token):
            domain_names = []
            for dn in self.domains:
                domain_names.append(dn['dn_name'])

            filterGraphListWidget.fillFilterGraphListWidget(domain_names)
            filterGraphListWidget.exec_()

            if filterGraphListWidget.target == None or filterGraphListWidget.target == "" :
                return

            domain = filterGraphListWidget.target

            self.listAllSubdomainsForDomain(self.apiHost, self.apiPort, domain, self.token)

            rectX = 10
            rectY = 0
            rectWidth = 0
            rectHeight = 50

            rects = []

            self.listAllSubdomainsForDomain(self.apiHost, self.apiPort, domain, self.token)

            domainX = (len(self.domain['subdomains']) * 200)/2

            #domainY = -2000
            domainY = 0
            rectWidth = len(domain) * 10
            rectX = rectWidth + 50

            domain_rect = self.drawRect(domainX, domainY, rectWidth, rectHeight, domain, self.greenBrush, False)
            domainrect = self.objectsGraphicScene.addItem(domain_rect)
            #domainR = domainrect.geometry()
            #rects.append(domainrect)

            #rectY = -60 * int(len(self.domain['subdomains'])/2)


            for i in range(1, int(len(self.domain['subdomains']))):
                rectWidth = len(self.domain['subdomains'][i])*10
                rectX = len(self.domain['subdomains'][i])*10 + 50
                rectY += 60
                subdomainrect = self.drawRect(rectX, rectY, rectWidth, rectHeight, self.domain['subdomains'][i], self.redBrush, False)
                #rects.append(subdomainrect)

                self.createLineItem(domain_rect, subdomainrect, domainX, domainY, rectX, rectY)

                #rectWidth = len(self.domain['subdomains'][i+1])*10

            '''
            for i in range(int(len(self.domain['subdomains'])/2), int(len(self.domain['subdomains'])/2)+1):
                rectX = rectWidth + 50
                #rectY -= 60
                subdomainrect = self.drawRect(rectX, rectY, rectWidth, rectHeight, self.domain['subdomains'][i], self.redBrush)
                #rects.append(subdomainrect)
                self.createLineItem(domain_rect, subdomainrect, domainX, domainY, rectX, rectY)
                rectX = rectWidth + 50
                rectWidth = len(self.domain['subdomains'][i+1])*10
            '''
            #self.createLineItem(domain_rect, subdomainrect)

        #for i in range(1, len(rects)):
            #subdomainR = subdomain_rect.geometry()

            #.pos().x()

            '''
            self.objectsGraphicScene.addLine(
                    domainR.x() + domainR.width() / 2,
                    domainR.y() + domainR.height() / 2,

                    subdomainR.x() + subdomainR.width() / 2,
                    subdomainR.y() + subdomainR.height() / 2
                    )
            '''



            #self.objectsGraphicScene.addItem(rects[i])

    def drawLine(self, sourceX, sourceY, destX, destY):
        self.objectsGraphicScene.addLine(
                    sourceX + 150 / 2,
                    sourceY + 50 / 2,

                    destX + 100 / 2,
                    destY+ 50 / 2
                )

    def createLineItem(self, source, dest, sourceX, sourceY, destX, destY):
        import pyqtgraph

        line = QGraphicsLineItem(
            sourceX + 75,
            sourceY + 50,

            destX + 75,
            destY
        )
        line.setPen(pyqtgraph.mkPen(color=(0,0,0), width=1))

        self.objectsGraphicScene.addItem(line)

    def drawRect(self, count1, count2, count3, count4, labelname, brush, movable):
        #userEllipse = self.objectsGraphicScene.addRect(count1,count1, count2, count3, self.blackPen, self.greenBrush)
        rect = QGraphicsRectItem(count1, count2, count3, count4)
        if movable:
            rect.setFlag(QGraphicsItem.ItemIsMovable)
        #rect.setPos(100, 100)
        self.addLabel(rect, labelname, brush)
        return rect

    def drawEllipse(self, count1, count2, count3, count4, labelname, brush):
        #userEllipse = self.objectsGraphicScene.addRect(count1,count1, count2, count3, self.blackPen, self.greenBrush)
        rect = QGraphicsEllipseItem(count1, count2, count3, count4)
        if movable:
            rect.setFlag(QGraphicsItem.ItemIsMovable)
        #rect.setPos(100, 100)
        self.addLabel(rect, labelname, brush)
        #rect.setFlag(QGraphicsItem.ItemIsSelectable)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        return rect

    def addLabel(self, rect, labelname, brush):
        rect.setBrush(brush)

        rect.setFlag(QGraphicsItem.ItemIsSelectable)
        #
        #rect.setFlags(QGraphicsItem.ItemSendsGeometryChanges)

        label = QtWidgets.QLabel(labelname, alignment=QtCore.Qt.AlignLeft)
        label.setAutoFillBackground(False)
        #label.setWordWrap(True)
        label.setStyleSheet('background-color: transparent')
        font = QtGui.QFont('Times', 8)
        font.setBold(True)
        label.setFont(font)

        proxy = QtWidgets.QGraphicsProxyWidget(rect)
        proxy.setWidget(label)
        label.setAlignment(Qt.AlignCenter)
        #rect.boundingRect().left(),
        proxy.setPos(rect.boundingRect().left(), rect.boundingRect().top())

        self.objectsGraphicScene.addItem(rect)
        #self.objectsGraphicScene.addItem(proxy)

