#! /usr/bin/python3
# Character Encoding: UTF-8
#coding=utf-8

from PyQt5.QtCore import QAbstractTableModel, QTimer, Qt
from PyQt5.QtGui import QColor

class LogTableModel(QAbstractTableModel):
    """
    keep the method names
    they are an integral part of the model
    """
    thread = None
    pid = None
    parent = None
    def __init__(self, parent, mylist, header, pid, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.parent = parent
        self.pid = pid
        self.thread = mylist
        lines = []
        for line in mylist.parsed_lines:
            lines.append([v for k,v in line.items()])

        self.mylist = lines
        self.header = header
        self.timer = QTimer()
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
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(0), self.columnCount(0))
        )
        self.layoutChanged.emit()

    def updateModel(self):
        lines = []
        for line in self.thread.parsed_lines:
            lines.append([v for k,v in line.items()])

        self.mylist = lines
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(0), self.columnCount(0))
        )
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

        if role == Qt.BackgroundRole:
            if index.row() == 2:
                return QColor(200, 255, 230)
        elif role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
