import unittest
import requests
from pprint import pprint

import os, time, json
import subprocess
import shutil

class FunctionalTestCase(unittest.TestCase):
    dir_project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    def get_tails_running_count(self):
        proc = subprocess.Popen(
            ['ps aux', '-l'],
            stdout = subprocess.PIPE,
            stdin = subprocess.PIPE,
            shell = True
        )
        processes = proc.stdout.readlines()

        proc.stdout.close()
        proc.stdin.close()
        
        matching_processes = 0
        for process in processes:
            process_string = str(process)
            if 'fixtures/simple1.log' in process_string and 'tail ' in process_string:
                matching_processes+= 1

        return matching_processes

    def start(self, file_path):
        program_path = os.path.join(self.dir_project_root, 'blue-log-viewer1.py')
        proc = subprocess.Popen(
            ['python3', program_path, file_path],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        time.sleep(1)

        proc.stdout.close()
        proc.stderr.close()

    def exec_in_app(self, cmd):
        response = requests.post(url = 'http://localhost:8032/', json = {
            'command': cmd
        })

        try:
            return response.json()['result']
        except json.decoder.JSONDecodeError:
            return None

    def kill(self):
        self.exec_in_app('self.main_window.close()')

if __name__ == '__main__':
    unittest.main()