# This Python file uses the following encoding: utf-8

import requests
import json
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QSizePolicy, QMessageBox

class AddCredentials(QtWidgets.QDialog):
    awsSessionTokenState = False

    token = ""
    apiHost = ""
    apiPort = ""
    workspace = ""

    current_credentials = ""

    def __init__(self, token, apiHost, apiPort, workspace):
        super(AddCredentials, self).__init__()
        uic.loadUi("addCredentialWindow.ui", self)
        self.setFixedSize(self.size())

        self.token = token
        self.apiHost = apiHost
        self.apiPort = apiPort
        self.workspace = workspace

        self.awsHasSessionCheckBox.stateChanged.connect(self.enableAWSSessionTokenTextEdit)
        self.addAWSCredsPushButton.clicked.connect(self.setAWSCredentials)

    def setTeamserverSettings(self, token, apiHost, apiPort, workspace):
        self.token = token
        self.apiHost = apiHost
        self.apiPort = apiPort
        self.workspace = workspace

    def enableAWSSessionTokenTextEdit(self):
        self.awsSessionTokenState = not self.awsSessionTokenState
        self.awsSessionTokenTextEdit.setEnabled(self.awsSessionTokenState)

    def setAWSCredentials(self):
        access_key_id = self.awsAccessKeyLineEdit.text()
        secret_key = self.awsSecretKeyLineEdit.text()
        region = self.awsRegionLineEdit.text()

        sess_test = {}

        sess_test['profile'] = self.awsNameLineEdit.text()
        sess_test['access_key_id'] = str(access_key_id)
        sess_test['secret_key'] = str(secret_key)
        sess_test['region'] = region

        set_aws_creds_body = {
                "aws_profile_name": sess_test['profile'],
                "aws_access_key": sess_test['access_key_id'],
                "aws_secret_key": sess_test['secret_key'],
                "aws_region": region
        }

        if self.awsHasSessionCheckBox.isChecked():
            if str(self.awsSessionTokenTextEdit.toPlainText() == ""):
                msg = QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('logo.png'))
                msg.setWindowTitle("Error")
                msg.setText("Session Token is empty. Either put session token or uncheck the checkbox")
                msg.exec_()
                del(msg)
            else:
                sess_token = self.awsSessionTokenTextEdit.toPlainText()
                sess_test['session_token'] = sess_token
                set_aws_creds_body["aws_session_token"] = sess_token

        if sess_test['profile'] == "" or sess_test['access_key_id'] == "" or sess_test['secret_key'] == "" or sess_test['region'] == "":
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon('logo.png'))
            msg.setWindowTitle("Error")
            msg.setText("Please fill all the fields")
            msg.exec_()
            del(msg)

        else:
            aws_response = requests.post("http://{}:{}/api/latest/awscredentials".format(self.apiHost, self.apiPort),
                                     headers={"Authorization": "Bearer {}".format(self.token)},
                                     json={"aws_profile_name": sess_test['profile']})

            aws_test = json.loads(aws_response.text)

            if not "error" in aws_test:
                msg = QMessageBox()
                msg.setWindowIcon(QtGui.QIcon('logo.png'))
                msg.setWindowTitle("Error")
                msg.setText("Credentials exist. Use another profile name!")
                msg.exec_()
                del(msg)

            else:
                cred_prof = sess_test['profile']

                set_creds = json.loads(requests.put("http://{}:{}/api/latest/awscredentials".format(self.apiHost, self.apiPort),
                                                           headers={"Authorization": "Bearer {}".format(self.token)},
                                                           json=set_aws_creds_body).text)

                if "error" in set_creds:
                    msg = QMessageBox()
                    msg.setWindowIcon(QtGui.QIcon('logo.png'))
                    msg.setWindowTitle("Error")
                    msg.setText("{}".format(set_creds['error']))
                    msg.exec_()
                    del(msg)

                else:
                    self.current_credentials = sess_test['profile']
                    infoText = "Credential '{}' successfully added.".format(cred_prof)

                    msg = QMessageBox()
                    msg.setWindowIcon(QtGui.QIcon('logo.png'))
                    msg.setWindowTitle("Successful")
                    msg.setText(infoText)
                    msg.exec_()
                    del(msg)

                    self.close()
