import os, re

class LineFormat:
    """
    Represents line headings and regex
    """
    regex = None
    fields = []
    headers = []

    def __init__(self, regex):
        self.regex = regex

        # Secondry regex to get the column names from the regex match groups
        # So actually regexing a regex
        self.fields =  re.findall('\?P\<(.*?)\>', regex)
        self.headers = [field.replace('_', ' ') for field in self.fields]


class Factory:
    """
    Given a file path will create
    the correct LineFormat with a regex for that file
    """
    def create(self, path):
        file_name = os.path.basename(path)
        if file_name == 'error.log':
            return LineFormat(
                #  [some date]                [:error]            [pid - ignored] [client xxx.xxx.xxx.xxx] message to EOL
                '^\[(?P<Timestamp>[^\]]+)\] \[(?P<Type>[^\]]+)\] '
                '\[(?:[^\]]+)\] \[client (?P<Client>[^\]]+)\] (?P<Message>.*)$')

        if file_name == 'access.log':
            return LineFormat(
                #  [host] [user-identifier] [userid] [date] [request line] [status] [size] [referer] [useragent]
                '^(?P<Host>.*?) (?P<User_Identifier>.*?) (?P<User_ID>.*?) '
                '\[(?P<Date>.*)\] "(?P<Request>.*?)" (?P<Status>.*?) '
                '(?P<Size>.*?) "(?P<Referer>.*?)" "(?P<UserAgent>.*?)"$')

        return LineFormat('^(?P<Line>.*?)$')