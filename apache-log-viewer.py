#! /usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication
from log_table_model import LogTableModel
from log_ui import Window
from log_poller import Line_Format, File, Line_Parser, Processor_Thread

line_format = Line_Format(
    '^\[(?P<Timestamp>[^\]]+)\] \[(?P<Type>[^\]]+)\] \[(?P<PID>[^\]]+)\] (?P<Message>.*)$')

log_file = File(sys.argv[1])
line_parser = Line_Parser(line_format)
log_data_processor = Processor_Thread(log_file, line_parser)
log_data_processor.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    Window(log_data_processor, line_format.fields).show()
    app.exec_()