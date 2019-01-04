#! /usr/bin/python3
"""
    Apache Log Viewer - View Apache's Log in a GUI
    This program is not related to Apache or the Apache Software Foundation in any way
    Copyright (C) 2018  Nicholas Shiell

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import sys
from PyQt5.QtWidgets import QApplication
from log_table_model import LogTableModel
from log_ui import Window, File_Dialog
from log_poller import Line_Format, File, Line_Parser, Processor_Thread
from argparse import ArgumentParser
import os

if __name__ == '__main__':
    parser = ArgumentParser(
        description='Show an autoupdating grid from Apache\'s Error Log'
    )

    parser.add_argument(
        'file',
        help=
        'The Path of the log file to tail',
        nargs='?'
    )

    parser.add_argument(
        '--is-dark',
        action='store_const',
        required=False,
        const=True,
        help='Whether to use dark colours (for dark themes)'
    )

    app = QApplication(sys.argv)
    args = parser.parse_args()
    w = Window(args.is_dark, args.file)
    w.show()
    w.start_polling()
    app.exec_()