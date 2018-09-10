#! /usr/bin/python3
# Character Encoding: UTF-8





''' pqt_tableview3.py
explore PyQT's QTableView Model
using QAbstractTableModel to present tabular data
allow table sorting by clicking on the header title

used the Anaconda package (comes with PyQt4) on OS X
(dns)
'''

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


class MyWindow(QWidget):
    def __init__(self, dataList, header, pid, *args):
        QWidget.__init__(self, *args)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(70, 150, 1326, 582)
        self.setWindowTitle("Click on the header to sort table")

        self.table_model = MyTableModel(self, dataList, header, pid)
        self.table_view = QTableView()
        #self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        
        
        
        
        
        ## works?????
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        # bind cell click to a method reference
        self.table_view.clicked.connect(self.showSelection)
        self.table_view.clicked.connect(self.selectRow)

        self.table_view.setModel(self.table_model)
        # enable sorting
        self.table_view.setSortingEnabled(True)

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

        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()
        self.parent.table_view.scrollToBottom()
        return None
        dataList2 = []
        if self.change_flag is True:
            dataList2 = [
                [QCheckBox("关"), 0, '063802', '01', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '063802', '02', 'cu1705,cu1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '063802', '03', 'zn1705,zn1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '063802', '04', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '063802', '01', 'zn1705,zn1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '063802', '02', 'ru1705,ru1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '063802', '02', 'ni1705,ni1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '063802', '01', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
            ]
            self.change_flag = False
        elif self.change_flag is False:
            dataList2 = [
                [QCheckBox("关"), 0, '058176', '01', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '058176', '02', 'cu1705,cu1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '058176', '03', 'zn1705,zn1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '058176', '04', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '058176', '01', 'zn1705,zn1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '058176', '02', 'ru1705,ru1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '058176', '02', 'ni1705,ni1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
                [QCheckBox("关"), 0, '058176', '01', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
            ]
            self.change_flag = True

        lines = []
        for line in mylist.parsed_lines:
            lines.append([v for k,v in line.items()])


        self.mylist = dataList2
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        value = self.mylist[index.row()][index.column()]
        #if (index.column() == 0):
        #    value = self.mylist[index.row()][index.column()].text()
        #else:
        #    value = self.mylist[index.row()][index.column()]
        if role == QtCore.Qt.EditRole:
            return value
        elif role == QtCore.Qt.DisplayRole:
            return value
        #elif role == QtCore.Qt.CheckStateRole:
            #if index.column() == 0:
            #    # print(">>> data() row,col = %d, %d" % (index.row(), index.column()))
            #    if self.mylist[index.row()][index.column()].isChecked():
            #        return QtCore.Qt.Checked
            #    else:
            #        return QtCore.Qt.Unchecked

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        # print(">>> sort() col = ", col)
        if col != 0:
            self.emit(SIGNAL("layoutAboutToBeChanged()"))
            self.mylist = sorted(self.mylist, key=operator.itemgetter(col))
            if order == Qt.DescendingOrder:
                self.mylist.reverse()
            self.emit(SIGNAL("layoutChanged()"))

    def flags(self, index):
        if not index.isValid():
            return None
        # print(">>> flags() index.column() = ", index.column())
        if index.column() == 0:
            # return Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsUserCheckable
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        # print(">>> setData() role = ", role)
        # print(">>> setData() index.column() = ", index.column())
        # print(">>> setData() value = ", value)
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            print(">>> setData() role = ", role)
            print(">>> setData() index.column() = ", index.column())
            if value == QtCore.Qt.Checked:
                self.mylist[index.row()][index.column()].setChecked(True)
                self.mylist[index.row()][index.column()].setText("开")
                # if studentInfos.size() > index.row():
                #     emit StudentInfoIsChecked(studentInfos[index.row()])     
            else:
                self.mylist[index.row()][index.column()].setChecked(False)
                self.mylist[index.row()][index.column()].setText("关")
        else:
            print(">>> setData() role = ", role)
            print(">>> setData() index.column() = ", index.column())
        # self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
        print(">>> setData() index.row = ", index.row())
        print(">>> setData() index.column = ", index.column())
        self.dataChanged.emit(index, index)
        return True

def timer_func(win, mylist):
    print(">>> timer_func()")
    win.table_model.setDataList(mylist)
    win.table_view.repaint()
    win.table_view.update()

# def timer_func(num):
#     print(">>> timer_func() num = ", num)




#match1 = re.findall('\?P\<(.*?)\>', apache_regex)
#pprint.pprint(match1)


#header = ['timestamp', 'type', 'PID', 'Client', 'Message']
#for v in match.groups():
#    print(v)
#    print('\n\n')

import time
import subprocess
import select

class Log_File:
    path = None
    pid = None

    def __init__(self, path):
        self.path = path

    def read_file(self):
        # file handle fh
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
# Make the editable
log_file = Log_File('/var/log/apache2/error.log')
line_parser = Line_Parser(line_format)
log_data_processor = Log_Data_Processor_Thread(log_file, line_parser)
log_data_processor.start()

if __name__ == '__main__':
    app = QApplication([])
    # you could process a CSV file to create this data
    #header = ['开关', '只平', '期货账号', '策略编号', '交易合约', '总持仓', '买持仓', '卖持仓', '持仓盈亏', '平仓盈亏', '手续费', '净盈亏', '成交量', '成交金额', 'A成交率', 'B成交率', '交易模型', '下单算法']
    header = ['timestamp', 'type', 'PID', 'Client', 'Message']
    # a list of (fname, lname, age, weight) tuples
    #checkbox1 = QCheckBox("关");
    #checkbox1.setChecked(True)
    #dataList = [
    #    [checkbox1, 0, '058176', '01', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
    #    [QCheckBox("关"), 0, '058176', '02', 'cu1705,cu1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
    #    [QCheckBox("关"), 0, '058176', '03', 'zn1705,zn1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
    #    [QCheckBox("关"), 0, '058176', '04', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
    #    [QCheckBox("关"), 0, '058176', '01', 'zn1705,zn1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
    #    [QCheckBox("关"), 0, '058176', '02', 'ru1705,ru1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
    #    [QCheckBox("关"), 0, '058176', '02', 'ni1705,ni1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
    #    [QCheckBox("关"), 0, '058176', '01', 'rb1705,rb1710', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'MA', '01'],
    #]

    dataList = []
    win = MyWindow(log_data_processor, line_format.fields, log_file.pid)
    win.show()
    # win.table_model.setDataList(dataList)
    # timer = threading.Timer(10, timer_func, (win, dataList2))
    # timer.start()
    app.exec_()