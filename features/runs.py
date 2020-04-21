import unittest
from pprint import pprint

import os, time
import shutil

from functional import FunctionalTestCase

class TestFeatures(FunctionalTestCase):
    """ Feature: Users can tail logs """

    """ Rule: There shouldn't be any running processes on quit """
    def stest_no_leftover_processes(self):
        """
            Given a log file
            When I load the file
            And then close the program
            Then there should be no leftover processes
        """

        processes_before = self.get_tails_running_count()

        fixture_path = os.path.join(
            self.dir_project_root,
            'fixtures',
            'simple1.log'
        )

        self.assertEqual(0, processes_before)

        self.start(fixture_path)

        processes_during = self.get_tails_running_count()

        self.kill()

        processes_after = self.get_tails_running_count()

        self.assertEqual(1, processes_during)
        self.assertEqual(0, processes_after)




    """ Rule: the user can see logs in realtime """

    def stest_shows_values_and_add(self):
        """
            Given a log file with contents
            When the file is loaded
            Then the contents should be visibile
            And when lines are added they should also be visibile
        """
        fixture_path = os.path.join(self.dir_project_root, 'fixtures', 'simple1.log')
        fixture_temp_path = os.path.join(self.fixture_temp_dir, 'simple.log')

        self.make_fixture_temp_dir()
        shutil.copy(fixture_path, fixture_temp_path)
        self.start(fixture_temp_path)

        self.assertEqual(
            'AAA', 
            self.exec_in_app('self.main_window.table_view.table_model.index(0, 0).data()')
        )

        self.assertEqual(
            'BBB', 
            self.exec_in_app('self.main_window.table_view.table_model.index(1, 0).data()')
        )

        self.assertEqual(
            'CCC', 
            self.exec_in_app('self.main_window.table_view.table_model.index(2, 0).data()')
        )

        self.assertEqual(
            3,
            self.exec_in_app(
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
            self.exec_in_app('self.main_window.table_view.table_model.index(0, 0).data()')
        )

        self.assertEqual(
            'BBB', 
            self.exec_in_app('self.main_window.table_view.table_model.index(1, 0).data()')
        )

        self.assertEqual(
            'CCC', 
            self.exec_in_app('self.main_window.table_view.table_model.index(2, 0).data()')
        )

        self.assertEqual(
            'XXX', 
            self.exec_in_app('self.main_window.table_view.table_model.index(3, 0).data()')
        )

        self.assertEqual(
            'YYY', 
            self.exec_in_app('self.main_window.table_view.table_model.index(4, 0).data()')
        )

        self.assertEqual(
            'ZZZ', 
            self.exec_in_app('self.main_window.table_view.table_model.index(5, 0).data()')
        )

        self.assertEqual(
            6,
            self.exec_in_app(
                'self.main_window.table_view.table_model.rowCount(\
                    self.main_window.table_view.table_model\
                )'
            )
        )



    """ Rule: new lines are shown in colours """

    def stest_shows_colors(self):
        """
            Given a light themed desktop
            And a log file with contents
            When the file is loaded
            Then the existing contents should not be highlighted
            And when lines are added they should be lighted in the first colour
        """
        fixture_path = os.path.join(self.dir_project_root, 'fixtures', 'simple1.log')
        fixture_temp_path = os.path.join(self.fixture_temp_dir, 'simple.log')

        self.make_fixture_temp_dir()
        shutil.copy(fixture_path, fixture_temp_path)
        self.start(fixture_temp_path, ['-stylesheet', 'fixtures/QTDark.stylesheet'])

        self.assertEqual(
            'AAA', 
            self.exec_in_app('self.main_window.table_view.table_model.index(0, 0).data()')
        )
        
        self.assertIsNone(self.exec_in_app(
            'self.main_window.table_view.table_model.index(0, 0).data(Qt.BackgroundRole).name()'
        ))

        self.assertEqual(
            'BBB', 
            self.exec_in_app('self.main_window.table_view.table_model.index(1, 0).data()')
        )

        self.assertIsNone(self.exec_in_app(
            'self.main_window.table_view.table_model.index(1, 0).data(Qt.BackgroundRole).name()'
        ))

        self.assertEqual(
            'CCC', 
            self.exec_in_app('self.main_window.table_view.table_model.index(2, 0).data()')
        )

        self.assertIsNone(self.exec_in_app(
            'self.main_window.table_view.table_model.index(2, 0).data(Qt.BackgroundRole).name()'
        ))

        self.assertEqual(
            3,
            self.exec_in_app(
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
            self.exec_in_app('self.main_window.table_view.table_model.index(0, 0).data()')
        )

        self.assertEqual(
            'BBB', 
            self.exec_in_app('self.main_window.table_view.table_model.index(1, 0).data()')
        )

        self.assertEqual(
            'CCC', 
            self.exec_in_app('self.main_window.table_view.table_model.index(2, 0).data()')
        )

        self.assertEqual(
            'XXX', 
            self.exec_in_app('self.main_window.table_view.table_model.index(3, 0).data()')
        )

        # Make this pass!!!!
        #self.assertEqual(
        #    '#002864',
        #    self.exec_in_app(
        #        'self.main_window.table_view.table_model.index(3, 0).data(Qt.BackgroundRole).name()'
        #    )
        #)

        self.assertEqual(
            'YYY', 
            self.exec_in_app('self.main_window.table_view.table_model.index(4, 0).data()')
        )

        self.assertEqual(
            '#002864',
            self.exec_in_app(
                'self.main_window.table_view.table_model.index(4, 0).data(Qt.BackgroundRole).name()'
            )
        )

        self.assertEqual(
            'ZZZ', 
            self.exec_in_app('self.main_window.table_view.table_model.index(5, 0).data()')
        )

        self.assertEqual(
            '#002864',
            self.exec_in_app(
                'self.main_window.table_view.table_model.index(5, 0).data(Qt.BackgroundRole).name()'
            )
        )

        self.assertEqual(
            6,
            self.exec_in_app(
                'self.main_window.table_view.table_model.rowCount(\
                    self.main_window.table_view.table_model\
                )'
            )
        )

if __name__ == '__main__':
    unittest.main()