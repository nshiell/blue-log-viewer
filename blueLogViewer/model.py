# Copyright (C) 2019  Nicholas Shiell
from PyQt5.QtCore import Qt, QSize, QAbstractTableModel

class LogTableModel(QAbstractTableModel):
    __dataModel = None

    def __init__(self, parent, dataModel, *args):
        self.__dataModel = dataModel
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
        return len(self.__dataModel.parsed_lines)

    def columnCount(self, parent):
        return len(self.__dataModel.headers)

    def data(self, index, role):
        """
        This method is called internally by QT
        Allows overwriting things like style
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self.__dataModel.get_value(index.column(), index.row())

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.__dataModel.headers[col]

        return None








class LogTableModel1(QAbstractTableModel):
    """
    keep the method names they are an integral part of the model
    The main god object for data storage and marshaling data to the GUI
    Stores most of the system state
    """

    # the thing that knows how to break up lines o ftext
    # Also knows the column header text
    log_data_processor = None

    table_row_span_setter = None

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

    is_dark = None

    def __init__(self, parent, log_data_processor, is_dark, *args):
        """
        Get the lines loaded by this point and copy them to the grid
        Set the header text
        Start a timer for updating
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.parent = parent
        self.log_data_processor = log_data_processor
        self.parsed_lines = log_data_processor.parsed_lines
        self.header = log_data_processor.line_parser.line_format.fields
        self.header_raw = [x.replace(' ', '_') for x in self.header]
        self._create_time()
        self.is_dark = is_dark
        self.color_list = Color_list(is_dark)

    def _create_time(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateModel)
        self.timer.start(1000)

    def _set_parsed_lines_from_processor_and_emit(self, log_data_processor):
        """
        Re-import ALL the data from the log_data_processor
        """
        self.parsed_lines = log_data_processor.parsed_lines
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

    def get_color(self):
        return self.color_list[self.current_new_color_index]

    def data(self, index, role):
        """
        This method is called internally by QT
        Allows overwriting things like style
        """
        if not index.isValid():
            return None

        row_no = index.row()
        value = self.parsed_lines[row_no][self.header_raw[index.column()]]

        # Needs to be lazy-loaded as the table view doesn't exist when
        # LogTableModel is instantiated
        if self.table_row_span_setter == None:
            self.table_row_span_setter = TableRowSpanSetter(
                self.log_data_processor.line_parser.line_format,
                self.parent.findChild(QTableView)
            )

        self.table_row_span_setter.set_span_for_row(
            index,
            self.parsed_lines[row_no]
        )

        if role == Qt.BackgroundRole:
            if row_no >= self.log_data_processor.log_file.old_lines:
                if row_no not in self.line_special_colors:
                    self.line_special_colors[row_no] = self.current_new_color_index

                return self.color_list[self.line_special_colors[row_no]]
            #else:
            #    if row_no % 2:
            #        from PyQt5.QtGui import QPalette
            #        c = self.parent.table_view.palette().color(QPalette.Background)
            #        return QColor(c.red() + 30, c.green() + 30, c.blue() + 30)
                    #self.parent.table_view.palette().color(QPalette.Background)

        if role == Qt.EditRole:
            return value

        if role == Qt.DisplayRole:
            return value

        if role == Qt.TextAlignmentRole:
            return Qt.AlignBaseline

        if value != None and role == Qt.FontRole and len(value) > 50:
            font = QFont()
            font.setPointSize(9)
            return font

        if value != None and role == Qt.ForegroundRole and len(value) > 50:
            color = QColor(128, 128, 128)
            return QVariant(QBrush(color))

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
























class Model:
    __tableModel = None
    path = None

    fields = ['aa_aa', 'bb_bb', 'cc_cc']
    headers = ['aa aa', 'bb bb', 'cc cc']

    parsed_lines = [{
        'aa_aa': 'AAAAA',
        'bb_bb': 'BBBBB',
        'cc_cc': 'CCCCC'
    },
    {
        'aa_aa': 'TTT',
        'bb_bb': 'jkhjkh',
        'cc_cc': 'kjhiyt8687yh'
    },
    {
        'aa_aa': 'EFWEF',
        'bb_bb': 'ZZZZ',
        'cc_cc': 'xxxx'
    }]

    def get_value(self, column, row):
        field = self.fields[column]
        return self.parsed_lines[row][field]

    #@property
    def create_table_model(self, window):
        if self.__tableModel == None:
            self.__tableModel = LogTableModel(window, self)

        return self.__tableModel