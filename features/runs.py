import unittest
import requests
from pprint import pprint

import os, time, json
import subprocess
import shutil

dir_project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

def get_tails_running_count():
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

def start(file_path):
    program_path = os.path.join(dir_project_root, 'blue-log-viewer1.py')
    proc = subprocess.Popen(
        ['python3', program_path, file_path],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )

    time.sleep(1)

    proc.stdout.close()
    proc.stderr.close()

def exec_in_app(cmd):
    response = requests.post(url = 'http://localhost:8032/', json = {
        'command': cmd
    })

    try:
        return response.json()['result']
    except json.decoder.JSONDecodeError:
        return None

def kill():
    exec_in_app('self.main_window.close()')

class TestFeatureRuns(unittest.TestCase):

    def test_can_show_an_unformatted_file(self):
        processes_before = get_tails_running_count()

        fixture_path = os.path.join(dir_project_root, 'fixtures', 'simple1.log')

        self.assertEqual(0, processes_before)

        start(fixture_path)

        processes_during = get_tails_running_count()

        kill()

        processes_after = get_tails_running_count()

        self.assertEqual(1, processes_during)
        self.assertEqual(0, processes_after)

    def test_shows_values(self):
        fixture_path = os.path.join(dir_project_root, 'fixtures', 'simple1.log')
        start(fixture_path)

        self.assertEqual(
            'AAA', 
            exec_in_app('self.main_window.table_view.table_model.index(0, 0).data()')
        )

        self.assertEqual(
            'BBB', 
            exec_in_app('self.main_window.table_view.table_model.index(1, 0).data()')
        )

        self.assertEqual(
            'CCC', 
            exec_in_app('self.main_window.table_view.table_model.index(2, 0).data()')
        )

        self.assertEqual(
            3,
            exec_in_app(
                'self.main_window.table_view.table_model.rowCount(\
                    self.main_window.table_view.table_model\
                )'
            )
        )

        self.assertTrue(True)
        kill()

    def test_shows_values_add(self):
        fixture_path = os.path.join(dir_project_root, 'fixtures', 'simple1.log')
        fixture_temp_dir = os.path.join(dir_project_root, 'fixtures-temp')
        fixture_temp_path = os.path.join(fixture_temp_dir, 'simple.log')

        if os.path.exists(fixture_temp_dir):
            shutil.rmtree(fixture_temp_dir)

        os.mkdir(fixture_temp_dir)
        shutil.copy(fixture_path, fixture_temp_path)
        start(fixture_temp_path)

        self.assertEqual(
            'AAA', 
            exec_in_app('self.main_window.table_view.table_model.index(0, 0).data()')
        )

        self.assertEqual(
            'BBB', 
            exec_in_app('self.main_window.table_view.table_model.index(1, 0).data()')
        )

        self.assertEqual(
            'CCC', 
            exec_in_app('self.main_window.table_view.table_model.index(2, 0).data()')
        )

        self.assertEqual(
            3,
            exec_in_app(
                'self.main_window.table_view.table_model.rowCount(\
                    self.main_window.table_view.table_model\
                )'
            )
        )

        myfile = open(fixture_temp_path, "a")
        myfile.write("\nXXX\n")
        myfile.write("YYY\n")
        myfile.write("ZZZ\n")
        myfile.close()

        time.sleep(.3)

        self.assertEqual(
            'AAA', 
            exec_in_app('self.main_window.table_view.table_model.index(0, 0).data()')
        )

        self.assertEqual(
            'BBB', 
            exec_in_app('self.main_window.table_view.table_model.index(1, 0).data()')
        )

        self.assertEqual(
            'CCC', 
            exec_in_app('self.main_window.table_view.table_model.index(2, 0).data()')
        )

        self.assertEqual(
            'XXX', 
            exec_in_app('self.main_window.table_view.table_model.index(3, 0).data()')
        )

        self.assertEqual(
            'YYY', 
            exec_in_app('self.main_window.table_view.table_model.index(4, 0).data()')
        )

        self.assertEqual(
            'ZZZ', 
            exec_in_app('self.main_window.table_view.table_model.index(5, 0).data()')
        )

        self.assertEqual(
            6,
            exec_in_app(
                'self.main_window.table_view.table_model.rowCount(\
                    self.main_window.table_view.table_model\
                )'
            )
        )

        shutil.rmtree(fixture_temp_dir)
        kill()

if __name__ == '__main__':
    unittest.main()