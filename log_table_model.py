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
    log_data_processor = None
    parent = None

    def __init__(self, parent, log_data_processor, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.parent = parent
        self.log_data_processor = log_data_processor
        lines = []
        for line in log_data_processor.parsed_lines:
            lines.append([v for k,v in line.items()])

        self.parsed_lines = lines
        self.header = self.log_data_processor.line_parser.line_format.fields
        self._create_time()
        self.change_flag = True

    def _create_time(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateModel)
        self.timer.start(1000)

    def _set_parsed_lines_from_processor_and_emit(self, log_data_processor):
        lines = []
        for line in log_data_processor.parsed_lines:
            lines.append([v for k,v in line.items()])

        self.parsed_lines = lines
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(0), self.columnCount(0))
        )
        self.layoutChanged.emit()

    def setDataList(self, log_data_processor):
        self._set_parsed_lines_from_processor_and_emit(log_data_processor)

    def updateModel(self):
        self._set_parsed_lines_from_processor_and_emit(self.log_data_processor)
        self.parent.table_view.scrollToBottom()

    def rowCount(self, parent):
        return len(self.parsed_lines)

    def columnCount(self, parent):
        return len(self.log_data_processor.line_parser.line_format.fields)

    def data(self, index, role):
        if not index.isValid():
            return None

        value = self.parsed_lines[index.row()][index.column()]

        if role == Qt.BackgroundRole:
            if index.row() == 2:
                return QColor(200, 255, 230)
            if index.row() >= self.log_data_processor.log_file.old_lines:
                return QColor(255, 220, 90)
            
        elif role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
