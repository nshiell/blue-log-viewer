# Copyright (C) 2019  Nicholas Shiell
from time import time
import threading, re, time, subprocess, select

# @todo remove reference to QT stuff from this file
from PyQt5.QtCore import QThread


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
        while True:
            line = fh.readline().replace('\n', '')
            if line:
                yield line

            # todo check that empty lines don't truncate the list
            if not line:
                break
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


    def get_lines(self):
        """
        Gets the existing lines then starts tail
        yields them out
        """
        for line in self.read_file():
            yield line
            self.old_lines = self.old_lines + 1
        
        for line in self.tail_file():
            yield line

    def tail_kill(self):
        """
        Call this at the end of the program
        """
        self.proc.kill()


class Line_Parser:
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


class Line_Format:
    """
    Represents line headings and regex
    """
    regex = None
    fields = []

    def __init__(self, regex):
        self.regex = regex

        # Secondry regex to get the column names from the regex match groups
        # So actually regexing a regex
        fields = re.findall('\?P\<(.*?)\>', regex)
        self.fields = [field.replace('_', ' ') for field in fields]


class Processor_Thread(QThread):
    """
    This thread will create an expanding array of parsed_lines
    as they are yeild'ed from the log_file
    Needs to extend QThread not normal python threading (I think)
    """

    # Every line that is shown on screen
    parsed_lines = []
    # Instance of the File()
    log_file = None
    # Object that takes lines and knows how to make a data list out of them
    line_parser = None

    def __init__(self, log_file, line_parser):
        super().__init__()
        self.log_file = log_file
        self.line_parser = line_parser

    def get_all_parsed_lines(self):
        return self.parsed_lines

    def run(self):
        """
        Each new yielded line gets stored in here
        """
        for line in self.log_file.get_lines():
            self.parsed_lines.append(self.line_parser.parse(line))
