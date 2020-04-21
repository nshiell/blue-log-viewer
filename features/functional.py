import unittest
import requests
from pprint import pprint

import os, time, json
import subprocess
import shutil

class FunctionalTestCase(unittest.TestCase):
    needs_killing = False

    dir_project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    fixture_temp_dir = os.path.join(
        dir_project_root,
        'fixtures-temp'
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

    def start(self, file_path, args=[]):
        program_path = os.path.join(self.dir_project_root, 'blue-log-viewer1.py')
        proc = subprocess.Popen(
            ['python3', program_path, file_path] + args,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        time.sleep(1)

        proc.stdout.close()
        proc.stderr.close()
        self.needs_killing = True

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
        self.needs_killing = False

    def tearDown(self):
        if self.needs_killing:
            self.kill()
            self.needs_killing = False

        if os.path.exists(self.fixture_temp_dir):
            shutil.rmtree(self.fixture_temp_dir)

    def make_fixture_temp_dir(self):
        if os.path.exists(self.fixture_temp_dir):
            shutil.rmtree(self.fixture_temp_dir)

        os.mkdir(self.fixture_temp_dir)


if __name__ == '__main__':
    unittest.main()