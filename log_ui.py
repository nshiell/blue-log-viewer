# Copyright (C) 2018  Nicholas Shiell
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
from log_table_model import LogTableModel
import os, signal
import log_poller
import sys

class File_Dialog:
    default_path = '/var/log'

    def get_valid_file_name(self, win):
        path_parts = QFileDialog.getOpenFileName(
            win,
            "Select log file",
            self.default_path
        )

        path = path_parts[0]
        if not path or not os.path.isfile(path):
            os._exit(0)

        return path

class Window_title:
    path = None

    def __init__(self, path):
        self.path = path

    def __str__(self):
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
    window = None

    def __init__(self, window):
        self.window = window

        w = window.findChild
        table_model = window.table_view.table_model

        w(QPushButton, 'color').clicked.connect(lambda:
            table_model.change_color()
        )

        w(QPushButton, 'tail').clicked.connect(lambda:
            w(QPushButton, 'tail').setText(
                'Tail ' + (
                    'Stop' if table_model.toggle_tail() else 'Start'
                )
            )
        )

        w(QTableView).doubleClicked.connect(lambda modeIndex:
            Line_QMessageBox()
                .set_line(
                    table_model.parsed_lines[modeIndex.row()],
                    modeIndex.row()
                )
                .exec_()
        )

    def window_close(self):
        self.window.table_view.table_model.log_data_processor.log_file.tail_kill()
        os._exit(0)


class QTableView_Log(QTableView):
    table_model = None

    def __init__(self):
        super().__init__()
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

    def setModel(self, model):
        self.table_model = model
        return super().setModel(model)

class Table_Model_Factory:
    def create(self, window, args):
        file_path = args.file
        if not file_path:
            file_path = File_Dialog().get_valid_file_name(window)

        log_file = log_poller.File(file_path)

        line_format = log_poller.Line_Format(
            #  [some date]                [:error]            [pid - ignored] [client xxx.xxx.xxx.xxx] message to EOL
            '^\[(?P<Timestamp>[^\]]+)\] \[(?P<Type>[^\]]+)\] \[(?:[^\]]+)\] \[client (?P<Client>[^\]]+)\] (?P<Message>.*)$')

        line_parser = log_poller.Line_Parser(line_format)
        log_data_processor = log_poller.Processor_Thread(log_file, line_parser)
        return LogTableModel(window, log_data_processor, args.is_dark)


class Window_Factory:
    def create(self, args):
        window = Window(Table_Model_Factory(), args)

        return window


class Window(QMainWindow):
    events = None
    table_view = None

    def __init__(self, table_model_factory, parsed_args, *args):
        super().__init__()

        table_model = table_model_factory.create(self, parsed_args)

        self.table_view = QTableView_Log()
        self.table_view.setModel(table_model)
        self.table_view.setColumsHeaderWidths()
        self._set_ui()
        self.events = Events(self)

    def start_polling(self):
        """
        Start reading the log onto the screen
        MUST be called after Window.show()
        """
        self.table_view.table_model.log_data_processor.start()

    def _set_ui(self):
        centralwidget = QWidget()

        self.setWindowTitle(str(Window_title(
            self.table_view.table_model.log_data_processor.log_file.path
        )))

        self.setGeometry(70, 150, 1326, 582)
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

    def closeEvent(self, event):
        event.accept()
        self.events.window_close()
