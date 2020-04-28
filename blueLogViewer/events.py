# Copyright (C) 2019  Nicholas Shiell
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer

class EventsBinder:
    """
    Bindings for the Window class
    Maybe there are other more standard ways of doing this - but it works
    The binding happens on __init__ and should be familiar to anyone that has
    used jQuery before
    """
    window = None
    window_color_changer = None
    log_file = None

    def __init__(self, window, log_file):
        self.window = window
        self.log_file = log_file

        if not window.table_view:
            raise TypeError('Call window.setup() before binding events')

        w = window.findChild
        self.window_color_changer = ColorChanger(
            window.table_view.table_model,
            w(QLabel, 'current_color'),
            w(QPushButton, 'color')
        )

        window.table_view.verticalScrollBar().setDisabled(True)
        self.bind(window, w)
        self.loop_tail()

    def loop_tail(self):
        self.window.table_view.scrollToBottom()
        self.timer = QTimer()

        self.timer.timeout.connect(lambda:
            self.scroll_to_bottom_if_needed()
        )
    
        self.timer.start(10)

    def scroll_to_bottom_if_needed(self):
        if self.window.table_view.table_model.keep_scroll_to_bottom:
            self.window.table_view.scrollToBottom()

    def bind(self, window, w):
        window.closed.connect(self.handle_close)
        window.is_now_visibile.connect(self.window_shown)

        w(QPushButton, 'color').clicked.connect(lambda:
            self.window_color_changer.change_and_update_ui()
        )

        w(QCheckBox, 'tail').clicked.connect(lambda:
            window.table_view.verticalScrollBar().setDisabled(
                self.window.table_view.table_model.toggle_tail()
            )
        )

        self.window.table_view.table_model.view = w(QTableView)
        w(QTableView).doubleClicked.connect(window.show_line_message_box)

    def window_shown(self):
        self.window.table_view.table_model.is_dark = self.window.is_dark
        self.window_color_changer.update_ui()

    def handle_close(self):
        """
        When closing the window the tail thread is killed
        and the program exists
        """
        self.log_file.tail_kill()
        os._exit(0)


class ColorChanger:
    table_model = None
    current_color_label = None
    color_button = None

    def __init__(self, table_model, current_color_label, color_button):
        self.table_model = table_model
        self.current_color_label = current_color_label
        self.color_button = color_button

    def get_border_color(self, color, is_dark, strength):
        if is_dark:
            return QColor(
                color.red() + strength,
                color.green() + strength,
                color.blue() + strength
            )

        return QColor(
            color.red() - strength,
            color.green() - strength,
            color.blue() - strength
        )

    def update_ui(self): 
        color = self.table_model.current_color
        highlight_color_low = self.get_border_color(
            color,
            self.table_model.is_dark,
            15
        )

        highlight_color_high = self.get_border_color(
            color,
            self.table_model.is_dark,
            80
        )

        self.current_color_label.setStyleSheet("""
            background-color: %s;
            border: 1px solid %s;
            color: %s;
            padding: 0 40px""" % (
                color.name(),
                highlight_color_low.name(),
                highlight_color_high.name())
        )

    def change_and_update_ui(self):
        self.table_model.change_color()
        self.update_ui()
