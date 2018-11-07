from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from log_table_model import LogTableModel
import os, signal
import log_poller
import sys

class Window_title:
    path = None

    @property
    def text(self):
        return '%s - Log Viewer' % self.path

class QTableView_Log(QTableView):
    def __init__(self):
        super().__init__()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.table_view.horizontalHeader().setStretchLastSection(QHeaderView.Stretch)

        ## works?????
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # bind cell click to a method reference
        #self.clicked.connect(QAbstractItemView.showSelection)
        #self.clicked.connect(QAbstractItemView.selectRow)

        self.setSortingEnabled(False)

class Window(QWidget):
    title = None

    def __init__(self, log_data_processor, header, *args):
        QWidget.__init__(self, *args)
        self.title = Window_title()
        self.title.path = log_data_processor.log_file.path
        self.setGeometry(70, 150, 1326, 582)
        self.setWindowTitle(self.title.text)

        self.table_model = LogTableModel(self, log_data_processor)

        self.table_view = QTableView_Log()
        self.table_view.setModel(self.table_model)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)
        self.setLayout(layout)
        self.table_view.scrollToBottom()

    def update_model(self, datalist, header):
        self.table_model2 = MyTableModel(self, dataList, header)
        self.table_view.setModel(self.table_model2)
        self.table_view.update()

    def showSelection(self, item):
        cellContent = item.data()
        # print(cellContent)  # test
        sf = "You clicked on {}".format(cellContent)
        # display in title bar for convenience
        self.setWindowTitle(sf)

    def selectRow(self, index):
        # print("current row is %d", index.row())
        pass

    def closeEvent(self, event):
        event.accept()
        os._exit(0)