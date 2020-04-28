# Copyright (C) 2019  Nicholas Shiell
from PyQt5.QtCore import Qt, QSize, QAbstractTableModel, QVariant
from PyQt5.QtGui import QBrush
from blueLogViewer.line_format import Factory as LineFormatFactory

import re, io, subprocess, select, time

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor

class File:
    """
    Represents a file that can be parsed - line by line
    uses "tail -f" for reading - so best use in a thread
    """
    path = None
    old_lines = 0
    proc = None

    def __init__(self, path):
        self.path = path

    def read_file(self):
        """
        Uses Pythons file reading lib for the initial scrape of the file
        """
        fh = open(self.path)
        for line in fh.readlines():
            yield line

        fh.close()

    def tail_file(self):
        """
        After the initial file read
        spawn tail -F   (to hold the file open)
                   -n 0 (to show new lines we don't know about)
        Each new line will get yielded out

        Don't forget to call self.tail_kill() when to program is done
        """
        self.proc = subprocess.Popen(['tail', '-F', '-n 0', self.path],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p = select.poll()
        p.register(self.proc.stdout)

        for line in io.TextIOWrapper(self.proc.stdout, encoding="utf-8"):
            if line.strip():
                yield line

    def tail_kill(self):
        """
        Call this at the end of the program
        """
        self.proc.kill()


class LineParser:
    """
    Given a Line_Format instance will create an array of data
    from a line
    """
    line_format = None

    def __init__(self, line_format):
        """
        line_format know the regex and field list - for headers
        """
        self.line_format = line_format

    def parse(self, line):
        """
        Given a line of text (without newline th the end)
        will return an array of data from the regex

        If the regex match fails - then the raw string will
        be the first field's data
        """
        match = re.search(self.line_format.regex, line)
        if match:
            return match.groupdict()

        # No match - set "None" into the array
        line_wrapped = dict((field, None) for field in self.line_format.fields)
        # ... and bung the raw line into the first field
        line_wrapped[self.line_format.fields[0]] = line
        return line_wrapped




class LineCollectionBroker():
    line_collection = None
    table_model = None
    _line_parser = None
    log_file = None
    tail_thread = None

    def __init__(self, path, window):
        self.log_file = File(path)

        line_format = LineFormatFactory().create(path)
        self.line_collection = LineCollection(line_format)
        self.table_model = LogTableModel(window, self.line_collection)
        
        self._line_parser = LineParser(line_format)

    def read_file_current_lines(self):
        for line in self.log_file.read_file():
            self.line_collection.add_line(self._line_parser.parse(line))

    def start_tailling(self):
        self.tail_thread = TailThread(self)
        self.tail_thread.start()
    
    def new_line(self, line):
        self.line_collection.add_line(self._line_parser.parse(line))
        self.table_model.update_emit()


class TailThread(QThread):
    sig = pyqtSignal(str)
    broker = None
    def __init__(self, broker, parent=None):
        self.broker = broker
        super().__init__(parent)
        self.sig.connect(broker.new_line)

    def run(self):
        for line in self.broker.log_file.tail_file():
            self.sig.emit(line)


class LogTableModel(QAbstractTableModel):
    """ Don't change these method names """
    keep_scroll_to_bottom = True
    _line_collection = None
    _table_row_span_setter = None

    def __init__(self, parent, line_collection, *args):
        self._line_collection = line_collection
        return super().__init__(parent, *args)

    def toggle_tail(self):
        self.keep_scroll_to_bottom = not self.keep_scroll_to_bottom
        return self.keep_scroll_to_bottom

    def update_emit(self):
        """
        We have updated data, tell Qt to do a re-update process
        """
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(self.rowCount(0), self.columnCount(0))
        )
        self.layoutChanged.emit()

    def rowCount(self, parent):
        return self._line_collection.get_lines_count()

    def columnCount(self, parent):
        return self._line_collection.get_headers_count()

    # @todo remove child reference from this class!
    view = None

    table_row_span_setter = None

    def data(self, index, role):
        """
        Allows overwriting things like style
        """
        if not index.isValid():
            return None


        # @todo rewrite this functionality
        # Needs to be lazy-loaded as the table view doesn't exist when
        # LogTableModel is instantiated
        if self.table_row_span_setter == None and self.view:
            self.table_row_span_setter = TableRowSpanSetter(
                self._line_collection.get_fields(),
                self.view
            )

        if self.table_row_span_setter:
            self.table_row_span_setter.set_span_for_row(
                index,
                self._line_collection.get_line(index.row())
            )

        value = self._line_collection.get_value(index.column(), index.row())

        if role == Qt.DisplayRole:
            return value

        if role == Qt.BackgroundRole:
            return self._line_collection.get_line_color(index.row())

        if value != None and role == Qt.ForegroundRole and len(value) > 50:
            color = QColor(128, 128, 128)
            return QVariant(QBrush(color))

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._line_collection.get_header(col)

        return None

    @property
    def is_dark(self):
        return self._line_collection.is_dark

    @is_dark.setter
    def is_dark(self, is_dark):
        self._line_collection.is_dark = is_dark

    def change_color(self):
        return self._line_collection.change_color()

    @property
    def current_color(self):
        return self._line_collection.current_color


class LineCollection:
    color_list = None
    current_new_color_index = 0

    _line_format = None
    _parsed_lines = []
    _line_colors = {}
    _is_dark = None

    def __init__(self, line_format):
        self._line_format = line_format

    def get_headers_count(self):
        return len(self._line_format.headers)

    def get_header(self, index):
        return self._line_format.headers[index]

    def get_lines_count(self):
        return len(self._parsed_lines)

    def get_line(self, row):
        return self._parsed_lines[row]

    def get_value(self, column, row):
        field = self._line_format.fields[column]
        return self._parsed_lines[row][field]

    def get_line_color(self, row):
        if row in self._line_colors:
            return self._line_colors[row]

    def add_line(self, parsed_line):
        if self.color_list:
            self._line_colors[len(self._parsed_lines)] = self.color_list[
                self.current_new_color_index]

        self._parsed_lines.append(parsed_line)

    def get_fields(self):
        return self._line_format.fields

    @property
    def is_dark(self):
        return self._is_dark

    @is_dark.setter
    def is_dark(self, is_dark):
        self._is_dark = is_dark
        self.color_list = ColorList(is_dark)

    def change_color(self):
        """
        Find the next color and set it to be used from now on
        """
        if self.color_list.len == self.current_new_color_index + 1:
            self.current_new_color_index = 0
        else:
            self.current_new_color_index += 1

    @property
    def current_color(self):
        return self.color_list[self.current_new_color_index]

class ColorList:
    """
    Represents the ordered set of background colors
    Will invert the colors - needed for dark themes
    """
    color_list = None

    def __init__(self, is_dark=False):
        if is_dark:
            self.color_list = [
                # Blueish
                QColor(0, 40, 100),

                # Redish
                QColor(100, 40, 40),

                # Greenish
                QColor(10, 70, 10)
            ]
        else:
            self.color_list = [
                # Blueish
                QColor(200, 220, 255),

                # Redish
                QColor(255, 210, 170),

                # Greenish
                QColor(200, 255, 170)
            ]

    def __getitem__(self, index):
        """
        Access members like this object is a list
        """
        return self.color_list[index]

    @property
    def len(self):
        return len(self.color_list)

class TableRowSpanSetter:
    """
    Represents a service which given a table view and a line format
    Will colspan a row if the line's data fails regex match
    i.e. all the data is in one cell
    """

    # So we ca make a visibile UI change
    table_view = None

    # best count out fields here, it's quicker doing it once
    column_count = None

    # best work out the second field name once, it's quicker doing it once
    second_field_name = None

    def __init__(self, fields, table_view):
        self.table_view = table_view
        self.column_count = len(fields)

        if self.column_count > 1:
            self.second_field_name = fields[1].replace(' ', '_')

    def set_span_for_row(self, index, data):
        if self.second_field_name and index.column() == 0 and data[self.second_field_name] == None:
            self.table_view.setSpan(index.row(), 0, 1, self.column_count)