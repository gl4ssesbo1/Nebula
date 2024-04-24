# This Python file uses the following encoding: utf-8

from PyQt5 import QtWidgets, uic, QtGui, QtCore

class FilterGraphListWidget(QtWidgets.QDialog):
    target = ""

    def __init__(self):
        super(FilterGraphListWidget, self).__init__()
        #self.load_ui()
        uic.loadUi("selectGraphFilterDialog.ui", self)

        title = "Select the target object"
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle(title)
        #self.show()
        self.filterGraphPushButton.clicked.connect(self.setTarget)


    def fillFilterGraphListWidget(self, jsonItem):
        for item in jsonItem:
            self.filterGraphListWidget.addItem(item)

    def setTarget(self):
        self.target = self.filterGraphListWidget.currentItem().text()
        self.close()
