import json
import codecs


from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    main_window = None

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        requestBody = self.rfile.read(content_length).decode("utf-8")
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = BytesIO()

        requestData = json.loads(requestBody)
        result = eval(requestData['command'])

        response.write(json.dumps({'result': result}).encode())
        self.wfile.write(response.getvalue())

def start(main_window):
    port = 8032

    SimpleHTTPRequestHandler.main_window = main_window

    print('listenning on port %d' % port)
    httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    httpd.serve_forever()