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
from log_ui import Window
from log_poller import Line_Format, File, Line_Parser, Processor_Thread
from argparse import ArgumentParser

class QApplication_Apache_Log_viewer(QApplication):
    args = None

    def __init__ (self, argv, args):
        self.args = args
        super().__init__(argv)

    def exec_(self):
        line_format = Line_Format(
            #  [some date]                [:error]            [pid - ignored] [client xxx.xxx.xxx.xxx] message to EOL
            '^\[(?P<Timestamp>[^\]]+)\] \[(?P<Type>[^\]]+)\] \[(?:[^\]]+)\] \[client (?P<Client>[^\]]+)\] (?P<Message>.*)$')

        log_file = File(self.args.file)
        line_parser = Line_Parser(line_format)
        log_data_processor = Processor_Thread(log_file, line_parser)
        log_data_processor.start()

        Window(log_data_processor, line_format.fields, self.args.is_dark).show()

        super().exec_()

if __name__ == '__main__':
    parser = ArgumentParser(
        description='Show an autoupdating grid from Apache\'s Error Log'
    )
    parser.add_argument("file", help="The Path of the log file to tail", nargs='?')

    parser.add_argument('--is-dark', action='store_const',
                        required=False,
                        const=True,
                        help='Whether to use dark colours (for dark themes)')

    QApplication_Apache_Log_viewer(sys.argv, parser.parse_args()).exec_()