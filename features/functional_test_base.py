import unittest, requests, os, time, json, subprocess, shutil, warnings

class FunctionalTestCase(unittest.TestCase):
    """ Extend unit testing to allow running out-of-process function tests """

    # The name of the python executable on your $PATH
    # change this if needed needs to be python >= 3
    python_exec_prefix = 'python3'


    # URL of where the app is running assumidly localhost
    rest_url = 'http://localhost:8032/'


    # Application needs to be killed in teardown?
    needs_killing = False


    # This suppreses warnoings
    # @todo remove the requirement to do this
    suppresed_warnings = False


    # Dir of the git checkout - all paths calcluated from here
    dir_project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )


    # Dir to put in fixtures that can be changed during the test
    fixture_temp_dir = os.path.join(
        dir_project_root,
        'fixtures-temp'
    )


    def get_tails_running_count(self):
        """ how many GNU/Tails are running? """

        proc = subprocess.Popen(
            'ps aux',
            stdout = subprocess.PIPE,
            stdin = subprocess.PIPE,
            shell = True
        )
        processes = proc.stdout.readlines()

        proc.stdout.close()
        proc.stdin.close()
        proc.wait()

        matching_processes = 0
        for process in processes:
            process_str = str(process)
            if 'fixtures/simple1.log' in process_str and 'tail ' in process_str:
                matching_processes+= 1

        return matching_processes


    def start(self, file_path, args=[]):
        """ Start blue-log-viewer.py in test mode """
        if self.suppresed_warnings == False:
            warnings.filterwarnings("ignore", category=ResourceWarning)
            self.suppresed_warnings = True

        program_path = os.path.join(self.dir_project_root, 'blue-log-viewer1.py')
        proc = subprocess.Popen(
            [self.python_exec_prefix, program_path, file_path] + args,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        time.sleep(2)

        proc.stdout.close()
        proc.stderr.close()
        self.needs_killing = True


    def exec_in_app(self, cmd):
        """ Send a RESTful request to the system under test
            eval the command and return the results
        """

        response = requests.post(url = self.rest_url, json = {'command': cmd})

        try:
            return response.json()['result']
        except json.decoder.JSONDecodeError:
            return None


    def kill(self):
        """ ASk the window to close """
        self.exec_in_app('self.main_window.close()')
        self.needs_killing = False


    def tearDown(self):
        """ Runs after each test,
            kills the app,
            destroys the temp fixtues dir
        """

        if self.needs_killing:
            self.kill()
            self.needs_killing = False

        if os.path.exists(self.fixture_temp_dir):
            shutil.rmtree(self.fixture_temp_dir)


    def make_fixture_temp_dir(self):
        if os.path.exists(self.fixture_temp_dir):
            shutil.rmtree(self.fixture_temp_dir)

        os.mkdir(self.fixture_temp_dir)