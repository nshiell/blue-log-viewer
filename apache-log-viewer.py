#! /usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication
from log_table_model import LogTableModel
from log_ui import Window
from log_poller import Line_Format, File, Line_Parser, Processor_Thread
from argparse import ArgumentParser

parser = ArgumentParser(
    description='Show an autoupdating grid from Apache\'s Error Log'
)
parser.add_argument("file", help="The Path of the log file to tail", nargs='?')

parser.add_argument('--is-dark', action='store_const',
                    required=False,
                    const=True,
                    help='Whether to use dark colours (for dark themes)')

args = parser.parse_args()

line_format = Line_Format(
    #  [some date]                [:error]            [pid - ignored] [client xxx.xxx.xxx.xxx] message to EOL
    '^\[(?P<Timestamp>[^\]]+)\] \[(?P<Type>[^\]]+)\] \[(?:[^\]]+)\] \[client (?P<Client>[^\]]+)\] (?P<Message>.*)$')

log_file = File(args.file)
line_parser = Line_Parser(line_format)
log_data_processor = Processor_Thread(log_file, line_parser)
log_data_processor.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    Window(log_data_processor, line_format.fields, args.is_dark).show()
    app.exec_()