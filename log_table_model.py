#! /usr/bin/python3
# Character Encoding: UTF-8
#coding=utf-8
# Copyright (C) 2019  Nicholas Shiell

from PyQt5.QtCore import QAbstractTableModel, QTimer, Qt
from PyQt5.QtGui import QColor

class Color_list:
    """
    Represents the ordered set of background colors
    Will invert the colors - needed for dark themes
    """
    color_list = [
        # Redish
        QColor(255, 230, 190),
        # Greenish
        QColor(190, 255, 230),
        # Blueish
        QColor(230, 190, 255)
    ]

    def __init__(self, is_dark=False):
        # Dark theme - then flip the color values
        if is_dark:
            color_list = []
            for color in self.color_list:
                color_list.append(QColor(
                    255 - color.red(),
                    255 - color.green(),
                    255 - color.blue()
                ))
            self.color_list = color_list

    def __getitem__(self, index):
        """
        Access members like this object is a list
        """
        return self.color_list[index]

    @property
    def len(self):
        return len(self.color_list)

class LogTableModel(QAbstractTableModel):
    """
    keep the method names they are an integral part of the model
    The main god object for data storage and marshaling data to the GUI
    Stores most of the system state
    """

    # the thing that knows how to break up lines o ftext
    # Also knows the column header text
    log_data_processor = None

    # the window where the grid object is shown
    parent = None

    # For rotating colors
    current_new_color_index = 0

    # dict of which lines have special colors applied
    # - needs to be stored as the data is refreshed
    line_special_colors = {}
    color_list = None

    # If true hold the grid scrolled at the last row
    hold_tail = True

    def __init__(self, parent, log_data_processor, is_dark, *args):
        """
        Get the lines loaded by this point and copy them to the grid
        Set the header text
        Start a timer for updating
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.parent = parent
        self.log_data_processor = log_data_processor
        lines = []
        for line in log_data_processor.parsed_lines:
            lines.append([v for k,v in line.items()])

        self.parsed_lines = lines
        self.header = log_data_processor.line_parser.line_format.fields
        self._create_time()
        self.color_list = Color_list(is_dark)

    def _create_time(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateModel)
        self.timer.start(1000)

    def _set_parsed_lines_from_processor_and_emit(self, log_data_processor):
        """
        Re-import ALL the data from the log_data_processor
        """
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

    def toggle_tail(self):
        self.hold_tail = not self.hold_tail
        return self.hold_tail

    def setDataList(self, log_data_processor):
        self._set_parsed_lines_from_processor_and_emit(log_data_processor)

    def updateModel(self):
        self._set_parsed_lines_from_processor_and_emit(self.log_data_processor)
        if self.hold_tail:
            self.parent.table_view.scrollToBottom()

    def rowCount(self, parent):
        return len(self.parsed_lines)

    def columnCount(self, parent):
        return len(self.log_data_processor.line_parser.line_format.fields)

    def change_color(self):
        """
        Find the next color and set it to be used from now on
        """
        if self.color_list.len == self.current_new_color_index + 1:
            self.current_new_color_index = 0
        else:
            self.current_new_color_index += 1

    def data(self, index, role):
        """
        This method is called internally by QT
        Allows overwriting things like style
        """
        if not index.isValid():
            return None

        row_no = index.row()
        value = self.parsed_lines[row_no][index.column()]

        if role == Qt.BackgroundRole:
            if row_no >= self.log_data_processor.log_file.old_lines:
                if row_no not in self.line_special_colors:
                    self.line_special_colors[row_no] = self.current_new_color_index

                return self.color_list[self.line_special_colors[row_no]]
        elif role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
