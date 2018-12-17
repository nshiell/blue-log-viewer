# Copyright (C) 2018  Nicholas Shiell
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from log_table_model import LogTableModel
import os, signal
import log_poller
import sys

class File_Dialog():
    default_path = '/var/log'

    def get_valid_file_name(self):
        path_parts = QFileDialog.getOpenFileName(None, "Select log file", self.default_path)
        path = path_parts[0]
        if not path or not os.path.isfile(path):
            os._exit(0)

        return path

class Window_title:
    path = None

    @property
    def text(self):
        return '%s - Log Viewer' % self.path

class Line_QMessageBox(QMessageBox):
    bullet = None

    def __init__(self):
        super().__init__()
        bullet = u"\u2022"
        self.bullet = '<br />    <span style="color: #AAAAAA">' + bullet + '</span> '

    def list_to_bullets(self, list_details):
        bullet_list = self.bullet.join(list_details)
        return self.bullet + bullet_list

    def set_line(self, parsed_line, row_no):
        self.setIcon(QMessageBox.Information)
        self.setText("Information about the item")
        self.setInformativeText(self.list_to_bullets(parsed_line[:-1]))
        self.setWindowTitle('Line %d Details' % row_no)
        self.setDetailedText(parsed_line[-1])
        self.setStandardButtons(QMessageBox.Cancel)

        return self

class Events:
    table_model = None

    def __init__(self, window):
        self.table_model = window.table_model
        w = window.findChild

        w(QPushButton, 'color').clicked.connect(lambda:
            self.table_model.change_color()
        )

        w(QPushButton, 'tail').clicked.connect(lambda:
            w(QPushButton, 'tail').setText(
                'Tail ' + (
                    'Stop' if self.table_model.toggle_tail() else 'Start'
                )
            )
        )

        w(QTableView).doubleClicked.connect(lambda modeIndex:
            Line_QMessageBox()
                .set_line(
                    self.table_model.parsed_lines[modeIndex.row()],
                    modeIndex.row()
                )
                .exec_()
        )

    def window_close(self):
        os._exit(0)

class QTableView_Log(QTableView):
    def __init__(self, events):
        super().__init__()
        self.events = events
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setSortingEnabled(False)

    def setColumsHeaderWidths(self):
        header = self.horizontalHeader()
        columnCount = header.count()
        for column in range(columnCount):
            if column != columnCount - 1:
                header.setSectionResizeMode(column, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(column, QHeaderView.Interactive)
            else:
                header.setSectionResizeMode(column, QHeaderView.Stretch)

class Window(QMainWindow):
    events = None
    keyPressed = QtCore.pyqtSignal(int)
    def __init__(self, log_data_processor, header, is_dark, *args):
        super().__init__()

        self.title = Window_title()
        self.title.path = log_data_processor.log_file.path
        self.setGeometry(70, 150, 1326, 582)
        self.setWindowTitle(self.title.text)

        self.table_model = LogTableModel(self, log_data_processor, is_dark)

        self.table_view = QTableView_Log(self.events)
        self.table_view.setModel(self.table_model)
        self.table_view.setColumsHeaderWidths()
        self._set_ui()
        self.events = Events(self)
        self.table_view.scrollToBottom()

    def _set_ui(self):
        centralwidget = QWidget()

        colorChangeButton = QPushButton("Change Colour")
        colorChangeButton.setObjectName('color')

        tailButton = QPushButton("Tail Stop")
        tailButton.setObjectName('tail')

        hbox = QHBoxLayout()
        hbox.addWidget(colorChangeButton)
        hbox.addWidget(tailButton)

        vbox = QVBoxLayout(centralwidget)
        vbox.addLayout(hbox)
        vbox.addWidget(self.table_view)

        self.setCentralWidget(centralwidget)

    def update_model(self, datalist, header):
        self.table_model2 = MyTableModel(self, dataList, header)
        self.table_view.setModel(self.table_model2)
        self.table_view.update()

    def closeEvent(self, event):
        event.accept()
        self.events.window_close()