import unittest
from pprint import pprint

import os, time
import shutil

from functional import FunctionalTestCase

class TestFeatures(FunctionalTestCase):

    def test_can_show_an_unformatted_file(self):
        processes_before = self.get_tails_running_count()

        fixture_path = os.path.join(self.dir_project_root, 'fixtures', 'simple1.log')

        self.assertEqual(0, processes_before)

        self.start(fixture_path)

        processes_during = self.get_tails_running_count()

        self.kill()

        processes_after = self.get_tails_running_count()

        self.assertEqual(1, processes_during)
        self.assertEqual(0, processes_after)

    def test_shows_values(self):
        fixture_path = os.path.join(self.dir_project_root, 'fixtures', 'simple1.log')
        self.start(fixture_path)

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

        self.assertTrue(True)
        self.kill()

    def test_shows_values_add(self):
        fixture_path = os.path.join(self.dir_project_root, 'fixtures', 'simple1.log')
        fixture_temp_dir = os.path.join(self.dir_project_root, 'fixtures-temp')
        fixture_temp_path = os.path.join(fixture_temp_dir, 'simple.log')

        if os.path.exists(fixture_temp_dir):
            shutil.rmtree(fixture_temp_dir)

        os.mkdir(fixture_temp_dir)
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

        shutil.rmtree(fixture_temp_dir)
        self.kill()

if __name__ == '__main__':
    unittest.main()