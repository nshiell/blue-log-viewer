from time import time
import threading, re, time, subprocess, select

class File:
    """
    Represents a file that can be parsed - line by line
    uses "tail -f" for reading - so best use in a thread
    """
    path = None
    old_lines = 0

    def __init__(self, path):
        self.path = path

    def read_file(self):
        fh = open(self.path)
        while True:
            line = fh.readline().replace('\n', '')
            if line:
                yield line

            if not line:
                break
        fh.close()

    def tail_file(self):
        f = subprocess.Popen(['tail', '-F', '-n 0', self.path],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p = select.poll()
        p.register(f.stdout)
        #self.pid = f.pid

        while True:
            if p.poll(1):
                line = f.stdout.readline().decode("utf-8").replace('\n', '')
                if line:
                    yield line
            time.sleep(1)


    def get_lines(self):
        for line in self.read_file():
            yield line
            self.old_lines = self.old_lines + 1
        
        for line in self.tail_file():
            yield line

class Line_Parser:
    """
    Given a Line_Format instance will create an array of data
    from a line
    """
    line_format = None

    def __init__(self, line_format):
        self.line_format = line_format

    def parse(self, line):
        match = re.search(self.line_format.regex, line)
        if match:
            return match.groupdict()

        line_wrapped = dict((field, None) for field in self.line_format.fields)
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

        fields = re.findall('\?P\<(.*?)\>', regex)
        self.fields = [field.replace('_', ' ') for field in fields]



class Processor_Thread(threading.Thread):
    """
    This thread will create an expanding array of parsed_lines
    as they are yeild'ed from the log_file
    """
    parsed_lines = []
    log_file = None
    line_parser = None

    def __init__(self, log_file, line_parser):
        super().__init__()
        self.log_file = log_file
        self.line_parser = line_parser

    def get_all_parsed_lines(self):
        return self.parsed_lines

    def run(self):
        for line in self.log_file.get_lines():
            self.parsed_lines.append(self.line_parser.parse(line))
