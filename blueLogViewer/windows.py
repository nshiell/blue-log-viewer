# Copyright (C) 2019  Nicholas Shiell
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QIcon

import os

_default_path = '/var/log'



class Line_QMessageBox(QMessageBox):
    """
    Show a QT dialog box with a textarea with the log
    """
    bullet = None
    headers = None

    def __init__(self, headers):
        super().__init__()
        self.headers = headers

    def set_line(self, parsed_line, row_no):
        """
        Set the parsed line
        """
        self.setIcon(QMessageBox.Information)
        self.setText("Information about the item")
        from pprint import pprint
        text = ''
        for field in self.headers:
            field_key = field.replace(' ', '_')
            if parsed_line[field_key]:
                text+= field + '\n' + parsed_line[field_key]
        self.setDetailedText(text)
        self.setInformativeText(text[:100])
        self.setWindowTitle('Line %d Details' % int(int(row_no) + 1))

        self.setStandardButtons(QMessageBox.Cancel)

        return self



def _show_file_path_error(path, reason):
    box = QMessageBox()
    box.setWindowTitle('Error - Blue Log Viewer')
    box.setIcon(QMessageBox.Critical)
    box.setText("Can't open: %s" % (path))
    box.setInformativeText(reason)
    box.exec_()


def get_valid_path(main_window, path):
    if not path:
        path_parts = QFileDialog.getOpenFileName(
            main_window,
            "Select log file",
            _default_path
        )

        path = path_parts[0]
        if not path or not os.path.isfile(path):
            os._exit(1)

    try:
        open(path)
    except IOError as e:
        _show_file_path_error(path, e.__class__.__name__)
        os._exit(1)

    return path


def app_icon_setter(app):
    """
    Sets the application icon
    Do it on the app not the main window as the window might not be shown
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_artwork = os.path.realpath(os.path.join(dir_path, '..', 'artwork'))

    icon_path = os.path.join(dir_artwork, 'blue-log-viewer.png')

    if os.path.isfile(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        print('Icon file not found: ' + icon_path)


class QTableViewLog(QTableView):
    """
    This model is the model for the grid layout
    NOT it's data store - it does encapsulate it in table_model though
    """

    # to avoid having to fish around in the inheritance chain to get this object
    # store a referecnce here
    table_model = None

    def __init__(self):
        super().__init__()
        # stretch out the colums as far as the UI widget (& window) will allow
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # no multi-select needed
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        # select rows - not cells or columns
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setWordWrap(False)
        # Sorting on lots of data is expensive
        # and everything should be chromologically ordered
        # This isn't an interactive analyser, just a read-only log view
        self.setSortingEnabled(False)

        #self.setColumsHeaderWidths()
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)


        # Disable scrollbars so it will be loocked to the bottom (tailed)
        #self.verticalScrollBar().setDisabled(True)
        self.verticalHeader().hide()

    def _configure_size_columns(self):
        """
        Overriding a QT method here - hence the naming
        All columns wont stretch out except the last one -
        as that one holds the data body
        """
        header = self.horizontalHeader()
        column_count = header.count()

        headerMode = header.setSectionResizeMode
        for column in range(column_count):
            if column != column_count - 1:
                headerMode(column, QHeaderView.ResizeToContents)
                headerMode(column, QHeaderView.Interactive)
            else:
                headerMode(column, QHeaderView.Stretch)

    def setModel(self, table_model):
        self.table_model = table_model
        super().setModel(table_model)
        self._configure_size_columns()

    @property
    def is_dark(self):
        return self.table_model.is_dark

    @is_dark.setter
    def is_dark(self, is_dark):
        self.table_model.is_dark = is_dark

class QMainWindowBlueLogViewer(QMainWindow):
    table_view = None
    is_now_visibile = pyqtSignal()
    closed = pyqtSignal()

    def setup(self, table_model):
        self.table_view = QTableViewLog()
        self.table_view.setModel(table_model)

        """
        Set the title,
        drtaw out the UI - boxes, buttons & data grid
        """
        centralwidget = QWidget()

        # Force to-string of the object
        #self.setWindowTitle(str(Window_title(
        #    self.table_view.table_model.log_data_processor.log_file.path
        #)))
        # Todo - think about storing this in a config somehow
        self.setGeometry(70, 150, 1200, 700)

        # English GB spelling (no I18N for now)
        color_change_button = QPushButton("Change the colour")
        color_change_button.setObjectName('color')

        current_color_label = QLabel('This is the colour of new log entries')
        current_color_label.setAlignment(Qt.AlignVCenter)
        current_color_label.setObjectName('current_color')

        tailCheckBox = QCheckBox("Tail bottom of log file")
        tailCheckBox.setObjectName('tail')
        tailCheckBox.setLayoutDirection(Qt.RightToLeft)
        tailCheckBox.setChecked(True)

        vbox = QVBoxLayout(centralwidget)
        vbox.addWidget(self.table_view)

        self.statusBar().addWidget(color_change_button)
        self.statusBar().addWidget(current_color_label)

        hint_label = QLabel('Double click on an entry to view details')
        hint_label.setStyleSheet("font-style: italic; font-size: 9px")
        self.statusBar().addPermanentWidget(hint_label)
        self.statusBar().addPermanentWidget(tailCheckBox)


        self.setCentralWidget(centralwidget)

    @property
    def is_dark(self):
        color = self.palette().color(QPalette.Background)
        average = (color.red() + color.green() + color.blue()) / 3

        return average <= 128

    def closeEvent(self, event):
        """
        Proxies over to the event class - easier this way I think
        """
        event.accept()
        self.closed.emit()

    def show_line_message_box(self, headers, parsed_line, row_no):
        #@todo implement
        Line_QMessageBox(headers).set_line(parsed_line, row_no).exec_()
