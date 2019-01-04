# Copyright (C) 2019  Nicholas Shiell
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from log_table_model import LogTableModel
import os
import log_poller


from window import Window

class Line_QMessageBox(QMessageBox):
    """
    Show a QT dialog box with a textarea with the log
    """
    bullet = None

    def __init__(self):
        super().__init__()
        bullet = u"\u2022"
        self.bullet = '<br />    <span style="color: #AAAAAA">' + bullet + '</span> '

    def list_to_bullets(self, list_details):
        """
        Collapse a list into an HTML bulletted list
        """
        bullet_list = self.bullet.join(list_details)
        return self.bullet + bullet_list

    def set_line(self, parsed_line, row_no):
        """
        Set the parsed line
        """
        self.setIcon(QMessageBox.Information)
        self.setText("Information about the item")
        self.setInformativeText(self.list_to_bullets(parsed_line[:-1]))
        self.setWindowTitle('Line %d Details' % row_no)
        self.setDetailedText(parsed_line[-1])
        self.setStandardButtons(QMessageBox.Cancel)

        return self

class Events:
    """
    Bindings for the Window class
    Maybe there are other more standard ways of doing this - but it works
    The binding happens on __init__ and should be familiar to anyone that has
    used jQuery before
    """
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
        """
        When closing the window the tail thread is killed
        and the program exists
        """
        (self
            .window
            .table_view
            .table_model
            .log_data_processor
            .log_file
            .tail_kill()
        )
        os._exit(0)


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


class Table_Model_Factory:
    """
    Creating the data model for the table view model is tricky!
    The window MUST exist as we might need a file dialog
    but the window can't be ready as it has no data
    So this ought to be used in the Window __init__ somehow

    For now has line_format (i.e. the thing that knows how to understand lines)
    setup before handing this object to the window
    as the window doesn't care how data is parsed
    """
    line_format = None

    def __init__(self, line_format):
        self.line_format = line_format

    def create(self, window, args):
        """
        Creates a LogTableModel and injects a data model into it
        """

        # First get a VALID path
        # - it needs the window in case it needs to show a dialog
        file_path = args.file
        if not file_path:
            file_path = File_Dialog().get_valid_file_name(window)

        # Create a file instance, and a parser and then
        # give both to the processor thread
        # the thread will be started by an external call to the window
        log_file = log_poller.File(file_path)

        line_parser = log_poller.Line_Parser(self.line_format)
        log_data_processor = log_poller.Processor_Thread(log_file, line_parser)
        return LogTableModel(window, log_data_processor, args.is_dark)


class Events_Factory:
    def create(self, window):
        return Events(window)


class Window_Factory:
    def create(self, line_format, args):
        return Window(
            Table_Model_Factory(line_format),
            Events_Factory(),
            args
        )