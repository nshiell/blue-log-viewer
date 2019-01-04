# Copyright (C) 2018  Nicholas Shiell
from PyQt5.QtWidgets import *


class Window_title:
    path = None

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return '%s - Log Viewer' % self.path


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
        column_count = header.count()

        headerMode = header.setSectionResizeMode
        for column in range(column_count):
            if column != column_count - 1:
                headerMode(column, QHeaderView.ResizeToContents)
                headerMode(column, QHeaderView.Interactive)
            else:
                headerMode(column, QHeaderView.Stretch)

    def setModel(self, model):
        self.table_model = model
        return super().setModel(model)


class Window(QMainWindow):
    events = None
    table_view = None

    def __init__(self, table_model_factory, events_factory, parsed_args, *args):
        super().__init__()

        table_model = table_model_factory.create(self, parsed_args)

        self.table_view = QTableView_Log()
        self.table_view.setModel(table_model)
        self.table_view.setColumsHeaderWidths()
        self._set_ui()
        self.events = events_factory.create(self)

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
