# Copyright (C) 2019  Nicholas Shiell
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Window_title:
    path = None

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return '%s - Blue Log Viewer' % self.path


class QTableView_Log(QTableView):
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

        # Sorting on lots of data is expensive
        # and everything should be chromologically ordered
        # This isn't an interactive analyser, just a read-only log view
        self.setSortingEnabled(False)

        # Disable scrollbars so it will be loocked to the bottom (tailed)
        self.verticalScrollBar().setDisabled(True)

    def setColumsHeaderWidths(self):
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

    def setModel(self, model):
        """
        Overriding a QT method here - hence the naming
        Keep a nice refercne to the model
        """
        self.table_model = model
        return super().setModel(model)


class Window(QMainWindow):
    """
    This represents the main window

    An instance of this class is needed for showing the file dialog
    hence why this class must be instantiated before trying to draw any dialogs

    This class must also be instatiated before polling any file
    (due to threading issues)

    This class doesn't define any event behaviour
    Not does it parse arguments

    The factory patten is used so that this class can avoid instantiating
    any other objects
    """
    events = None
    table_view = None

    def __init__(self, table_model_factory, events_factory, parsed_args, *args):
        super().__init__()

        # The table model reprents the state of the data that we know about
        # So everything variable: colors, rows, system state etc
        # it is injected into the table_view which is a property of this class
        # table_model also has the file instance, file path and column headers
        table_model = table_model_factory.create(self, parsed_args)

        self.table_view = QTableView_Log()
        self.table_view.setModel(table_model)
        self.table_view.setColumsHeaderWidths()
        self._set_ui()

        # bind all events
        self.events = events_factory.create(self)

    def start_polling(self):
        """
        Start reading the log onto the screen
        MUST be called after Window.show()

        Maybe refctor this to the event class?
        """
        self.table_view.table_model.log_data_processor.start()

    def _set_ui(self):
        """
        Set the title,
        drtaw out the UI - boxes, buttons & data grid
        """
        centralwidget = QWidget()

        # Force to-string of the object
        self.setWindowTitle(str(Window_title(
            self.table_view.table_model.log_data_processor.log_file.path
        )))
        # Todo - think about storing this in a config somehow
        self.setGeometry(70, 150, 1326, 582)
        # English GB spelling (no I18N for now)
        colorChangeButton = QPushButton("Change Colour")
        colorChangeButton.setObjectName('color')

        tailCheckBox = QCheckBox("Tail bottom of log file")
        tailCheckBox.setObjectName('tail')
        tailCheckBox.setLayoutDirection(Qt.RightToLeft)
        tailCheckBox.setChecked(True)

        hbox = QHBoxLayout()
        hbox.addWidget(colorChangeButton)
        hbox.addWidget(tailCheckBox)

        vbox = QVBoxLayout(centralwidget)
        vbox.addLayout(hbox)
        vbox.addWidget(self.table_view)

        self.setCentralWidget(centralwidget)

    def closeEvent(self, event):
        """
        Proxies over to the event class - easier this way I think
        """
        event.accept()
        self.events.window_close()
