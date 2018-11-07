#! /usr/bin/python3
# Character Encoding: UTF-8
#coding=utf-8

import operator  # used for sorting
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from time import time
import threading
import os, signal
import re
import pprint

import sys

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

        #self.setModel(self.table_model)
        # enable sorting
        self.setSortingEnabled(False)

class Window_title:
    path = None

    @property
    def text(self):
        return '%s - Log Viewer' % self.path

class Log_Window(QWidget):
    title = None

    def __init__(self, dataList, header, pid, *args):
        QWidget.__init__(self, *args)
        self.title = Window_title()
        self.title.path = 'sfgsdfg'
        self.setGeometry(70, 150, 1326, 582)
        self.setWindowTitle(self.title.text)

        self.table_model = MyTableModel(self, dataList, header, pid)

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
        #os.kill(self.table_model.pid, signal.SIGTERM)
        #pprint.pprint(self.table_model.pid)
        #self.table_model.thread.join()
        event.accept()
        os._exit(0)
        #sys.exit()
    #def keyPressEvent(self, event):
        #print('dfg')

class MyTableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    thread = None
    pid = None
    parent = None
    def __init__(self, parent, mylist, header, pid, *args):
        #self.setData((1, 1), QBrush(Qt.red), QtCore.Qt.BackgroundRole)
        QAbstractTableModel.__init__(self, parent, *args)
        self.parent = parent
        #self.mylist = mylist.parsed_lines
        self.pid = pid
        self.thread = mylist
        lines = []
        for line in mylist.parsed_lines:
            lines.append([v for k,v in line.items()])

        self.mylist = lines
        self.header = header
        self.timer = QtCore.QTimer()
        self.change_flag = True
        self.timer.timeout.connect(self.updateModel)
        self.timer.start(1000)
        
        # self.rowCheckStateMap = {}

    def setDataList(self, mylist):
        lines = []
        for line in mylist.parsed_lines:
            lines.append([v for k,v in line.items()])

        self.mylist = lines
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()

    def updateModel(self):
        lines = []
        for line in self.thread.parsed_lines:
            lines.append([v for k,v in line.items()])

        self.mylist = lines
#setStyleSheet
        #self.index(0, 0).setStyleSheet('background-color: red')
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()
        self.parent.table_view.scrollToBottom()

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None

        value = self.mylist[index.row()][index.column()]

        if role == QtCore.Qt.BackgroundRole:
            if index.row() == 2:
                return QColor(200, 255, 230)
                #return QtGui.setStyleSheet('')
        elif role == QtCore.Qt.EditRole:
            return value
        elif role == QtCore.Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

def timer_func(win, mylist):
    print(">>> timer_func()")
    win.table_model.setDataList(mylist)
    win.table_view.repaint()
    win.table_view.update()

import time
import subprocess
import select

class Log_File:
    path = None
    pid = None

    def __init__(self, path):
        self.path = path

    def read_file(self):
        fh = open(self.path)
        while True:
            line = fh.readline().replace('\n', '')
            if line:
                yield line

            if not line:
                break
        fh.close()

    def tail_file(self):
        f = subprocess.Popen(['tail', '-F', '-n 0', self.path],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p = select.poll()
        p.register(f.stdout)
        self.pid = f.pid

        while True:
            if p.poll(1):
                line = f.stdout.readline().decode("utf-8").replace('\n', '')
                if line:
                    yield line
            time.sleep(1)


    def get_lines(self):
        for line in self.read_file():
            yield line
        
        for line in self.tail_file():
            yield line

class Line_Parser:
    line_format = None

    def __init__(self, line_format):
        self.line_format = line_format

    def parse(self, line):
        match = re.search(self.line_format.regex, line)
        if match:
            return match.groupdict()

        line_wrapped = dict((field, None) for field in self.line_format.fields)
        line_wrapped[self.line_format.fields[0]] = line
        return line_wrapped
        #if self.line_format.fields[0]
        #print(line)

class Line_Format:
    regex = None
    fields = []

    def __init__(self, regex):
        self.regex = regex

        fields = re.findall('\?P\<(.*?)\>', regex)
        self.fields = [field.replace('_', ' ') for field in fields]



class Log_Data_Processor_Thread(threading.Thread):
    parsed_lines = []
    log_file = None
    line_parser = None

    def __init__(self, log_file, line_parser):
        super(Log_Data_Processor_Thread, self).__init__()
        self.log_file = log_file
        self.line_parser = line_parser

    def get_all_parsed_lines(self):
        return self.parsed_lines

    def run(self):
        for line in self.log_file.get_lines():
            self.parsed_lines.append(self.line_parser.parse(line))

line_format = Line_Format('^\[(?P<Timestamp>[^\]]+)\] \[(?P<Type>[^\]]+)\] \[(?P<PID>[^\]]+)\] (?P<Message>.*)$')

log_file = Log_File(sys.argv[1])
line_parser = Line_Parser(line_format)
log_data_processor = Log_Data_Processor_Thread(log_file, line_parser)
log_data_processor.start()

if __name__ == '__main__':
    app = QApplication([])
    header = ['timestamp', 'type', 'PID', 'Client', 'Message']

    dataList = []
    win = Log_Window(log_data_processor, line_format.fields, log_file.pid)
    win.show()
    # win.table_model.setDataList(dataList)
    # timer = threading.Timer(10, timer_func, (win, dataList2))
    # timer.start()
    app.exec_()