import unittest
import requests
from pprint import pprint

#boot_hook = None
import os, time
import subprocess

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
    subprocess.Popen(['python3', program_path, file_path])

class TestFeatureRuns(unittest.TestCase):

    def test_can_show_an_unformatted_file(self):
        processes_before = get_tails_running_count()

        fixture_path = os.path.join(dir_project_root, 'fixtures', 'simple1.log')

        self.assertEqual(0, processes_before)

        start(fixture_path)
        time.sleep(1)

        processes_during = get_tails_running_count()

        response = requests.post(url = 'http://localhost:8032/', json = {
            'command': 'self.main_window.close()'
        })

        processes_after = get_tails_running_count()

        self.assertEqual(1, processes_during)
        self.assertEqual(0, processes_after)

    def ggg(self):
        response = requests.post(url = 'http://localhost:8032/', json = {
            #'command': 'self.main_window.table_view.table_model.index(0, 0).data()'
            #'command': 'self.main_window.table_view.table_model.log_data_processor.log_file.tail_kill() and os._exit(0)'
            'command': 'os._exit(0)'
        })

        pprint(response.json())
        #self.assertEqual(3, table_model.rowCount(table_model))

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()