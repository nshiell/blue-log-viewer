# Copyright (C) 2019  Nicholas Shiell
from PyQt5.QtCore import Qt, QSize, QAbstractTableModel
from blueLogViewer.line_format import Factory as LineFormatFactory


import re

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal






class File:
    """
    Represents a file that can be parsed - line by line
    uses "tail -f" for reading - so best use in a thread
    """
    path = None
    old_lines = 0
    proc = None

    def __init__(self, path):
        self.path = path

    def read_file(self):
        """
        Uses Pythons file reading lib for the initial scrape of the file
        """
        fh = open(self.path)
        for line in fh.readlines():
            yield line

        fh.close()

    def tail_file(self):
        """
        After the initial file read
        spawn tail -F   (to hold the file open)
                   -n 0 (to show new lines we already know about)
        Each new line will get yielded out

        Don't forget to call self.tail_kill() when to program is done
        """
        self.proc = subprocess.Popen(['tail', '-F', '-n 0', self.path],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p = select.poll()
        p.register(self.proc.stdout)

        while True:
            if p.poll(1):
                line = (self
                    .proc
                    .stdout
                    .readline()
                    .decode("utf-8")
                    .replace('\n', '')
                )
                if line:
                    yield line
            time.sleep(1)


    #def get_lines(self):
    #    """
    #    Gets the existing lines then starts tail
    #    yields them out
    #    """
    #    for line in self.read_file():
    #        yield line
    #        self.old_lines = self.old_lines + 1
    #    
    #    for line in self.tail_file():
    #        yield line

    def tail_kill(self):
        """
        Call this at the end of the program
        """
        self.proc.kill()




class LineParser:
    """
    Given a Line_Format instance will create an array of data
    from a line
    """
    line_format = None

    def __init__(self, line_format):
        """
        line_format know the regex and field list - for headers
        """
        self.line_format = line_format

    def parse(self, line):
        """
        Given a line of text (without newline th the end)
        will return an array of data from the regex

        If the regex match fails - then the raw string will
        be the first field's data
        """
        match = re.search(self.line_format.regex, line)
        if match:
            return match.groupdict()

        # No match - set "None" into the array
        line_wrapped = dict((field, None) for field in self.line_format.fields)
        # ... and bung the raw line into the first field
        line_wrapped[self.line_format.fields[0]] = line
        return line_wrapped



class LineCollectionBroker():
    _path = None
    line_collection = None
    table_model = None
    _line_parser = None

    def __init__(self, path, window):
        self._path = path
        
        log_file = File(path)
        
        t = Thready(self)
        t.start()
        
        line_format = LineFormatFactory().create(path)
        self.line_collection = LineCollection(line_format)
        self.table_model = LogTableModel(window, self.line_collection)
        
        self._line_parser = LineParser(line_format)
        for line in log_file.read_file():
            self.line_collection.add_line(self._line_parser.parse(line))
    
    def new_line(self, line):
        print ('=====')
        print(line)
        self.line_collection.add_line(self._line_parser.parse(line))
        self.table_model.update_emit()

import time
def blah(line):
    print ('asdf')
    print(line)

class Thready(QThread):
    sig = pyqtSignal(str)
    broker = None
    def __init__(self, broker, parent=None):
        self.broker = broker
        super().__init__(parent)
        self.sig.connect(broker.new_line)

    def run(self):
        time.sleep(5)
        print ('thing')
        self.sig.emit('sfgsdfg')
        

#thready = Thready()
#thready.start()


class LogTableModel(QAbstractTableModel):
    """Don't change these method names"""
    __line_collection = None

    def __init__(self, parent, line_collection, *args):
        self.__line_collection = line_collection
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

    #def setDataList(self):
    #    self.update_emit()

    #def updateModel(self):
    #    self.update_emit()

    def rowCount(self, parent):
        return self.__line_collection.get_lines_count()

    def columnCount(self, parent):
        return self.__line_collection.get_headers_count()

    def data(self, index, role):
        """
        Allows overwriting things like style
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self.__line_collection.get_value(index.column(), index.row())

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.__line_collection.get_header(col)

        return None





class LineCollection:
    #_table_model = None
    #path = None

    _line_format = None

    _parsed_lines = []
    """[{
        'Timestamp': 'AAAAA',
        'Client': 'BBBBB',
        'Type': 'CCCCC',
        'Message': 'dddddd'
    },
    {
        'Timestamp': 'TTT',
        'Client': 'jkhjkh',
        'Type': 'kjhiyt8687yh',
        'Message': 'dddddd'
    },
    {
        'Timestamp': 'EFWEF',
        'Client': 'ZZZZ',
        'Type': 'xxxx',
        'Message': 'dddddd'
    }]"""

    def __init__(self, line_format):
        self._line_format = line_format

    def get_headers_count(self):
        return len(self._line_format.headers)

    def get_header(self, index):
        return self._line_format.headers[index]

    def get_lines_count(self):
        return len(self._parsed_lines)

    def get_value(self, column, row):
        field = self._line_format.fields[column]
        return self._parsed_lines[row][field]

    #def create_table_model(self, window):
    #    if not self.__line_format:
    #        self.__line_format = LineFormatFactory().create(self.path)

    #    if self.__table_model == None:
    #        self.__table_model = LogTableModel(window, self)

    #    return self.__table_model

#    def add_lines(self, parsed_lines):
#        self._parsed_lines = parsed_lines

    def add_line(self, parsed_line):
        self._parsed_lines.append(parsed_line)