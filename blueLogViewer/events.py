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
        #table_model = window.table_view.table_model

        #window_color_changer = Window_color_Changer(
        #    table_model,
        #    w(QLabel, 'current_color'),
        #    w(QPushButton, 'color')
        #)

        #window_color_changer.update_ui()

        self.bind(window, w)

    def bind(self, window, w):
        return None
        w(QPushButton, 'color').clicked.connect(lambda:
            window_color_changer.change_and_update_ui()
        )

        w(QCheckBox, 'tail').clicked.connect(lambda:
            window.table_view.verticalScrollBar().setDisabled(
                table_model.toggle_tail()
            )
        )

        w(QTableView).doubleClicked.connect(lambda modeIndex:
            Line_QMessageBox(table_model.header)
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