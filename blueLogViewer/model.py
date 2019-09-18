# Copyright (C) 2019  Nicholas Shiell
from PyQt5.QtCore import Qt, QSize, QAbstractTableModel
from blueLogViewer.line_format import Factory as LineFormatFactory


class LogTableModel(QAbstractTableModel):
    """Don't change these method names"""
    __line_collection = None

    def __init__(self, parent, line_collection, *args):
        self.__line_collection = line_collection
        return super().__init__(parent, *args)

    def update_emit(self):
        """
        Re-import ALL the data from the log_data_processor
        """
        #self.parsed_lines = log_data_processor.parsed_lines
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(0), self.columnCount(0))
        )
        self.layoutChanged.emit()

    def setDataList(self, log_data_processor):
        self.update_emit()

    def updateModel(self):
        self.update_emit()

    def rowCount(self, parent):
        return self.__line_collection.get_lines_count()

    def columnCount(self, parent):
        return self.__line_collection.get_headers_count()

    def data(self, index, role):
        """
        Allows overwriting things like style
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self.__line_collection.get_value(index.column(), index.row())

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.__line_collection.get_header(col)

        return None



class LineCollection:
    __table_model = None
    path = None

    __line_format = None

    __parsed_lines = [{
        'Timestamp': 'AAAAA',
        'Client': 'BBBBB',
        'Type': 'CCCCC',
        'Message': 'dddddd'
    },
    {
        'Timestamp': 'TTT',
        'Client': 'jkhjkh',
        'Type': 'kjhiyt8687yh',
        'Message': 'dddddd'
    },
    {
        'Timestamp': 'EFWEF',
        'Client': 'ZZZZ',
        'Type': 'xxxx',
        'Message': 'dddddd'
    }]

    def get_headers_count(self):
        return len(self.__line_format.headers)

    def get_header(self, index):
        return self.__line_format.headers[index]

    def get_lines_count(self):
        return len(self.__parsed_lines)

    def get_value(self, column, row):
        field = self.__line_format.fields[column]
        return self.__parsed_lines[row][field]

    def create_table_model(self, window):
        if not self.__line_format:
            self.__line_format = LineFormatFactory().create(self.path)

        if self.__table_model == None:
            self.__table_model = LogTableModel(window, self)

        return self.__table_model