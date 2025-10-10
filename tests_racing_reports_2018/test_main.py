###### import tools ######
import unittest, datetime
from unittest.mock import patch, mock_open
import racing_reports_2018 as code


# test class for main.py
class TestMain(unittest.TestCase):
    """ Test class for main.py functions."""
    def setUp(self):
        # for test_get_datetime_info
        self.test_cases_datetime = [
            ('SVF2018-05-24_12:02:58.917\nNHR2018-05-24_12:02:49.914',
              {'SVF': datetime.datetime.fromisoformat('2018-05-24T12:02:58.917'),
               'NHR': datetime.datetime.fromisoformat('2018-05-24T12:02:49.914')}),
            ('SVF 2018-05-24_12:02:58.917\nNHR2018-05-24_12:02:49.914',             # fail
              {'NHR': datetime.datetime.fromisoformat('2018-05-24T12:02:49.914')}),
            (' \nNHR2018-05-24_12:02:49.914',                                       # fail
              {'NHR': datetime.datetime.fromisoformat('2018-05-24T12:02:49.914')}),]

        # for test_get_drivers_info
        self.test_cases_driver = [
            ((('DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER\n'
              'SVF_Sebastian Vettel_FERRARI\n'
              'SPF Sergio Perez_FORCE INDIA MERCEDES\n' # fail
              ' \n'
              'SVM_Stoffel Vandoorne_MCLAREN RENAULT\n'),                                   # fail
             {'DRR': datetime.datetime.fromisoformat('2018-05-24T12:14:12.054'),
               'SVF': datetime.datetime.fromisoformat('2018-05-24T12:02:58.917'),
               'SPF': datetime.datetime.fromisoformat('2018-05-24_12:12:01.035'),
               'CSR': datetime.datetime.fromisoformat('2018-05-24T12:03:15.145')},
             {'DRR': datetime.datetime.fromisoformat('2018-05-24T12:11:24.067'),
              'SVF': datetime.datetime.fromisoformat('2018-05-24T12:04:03.332'),
              'SPF': datetime.datetime.fromisoformat('2018-05-24_12:13:13.883'),
              'CSR': datetime.datetime.fromisoformat('2018-05-24T12:04:28.095')}),
            # for test class objects
            (('DRR',
              'Daniel Ricciardo',
              'RED BULL RACING TAG HEUER',
              datetime.datetime.fromisoformat('2018-05-24T12:14:12.054'),
              datetime.datetime.fromisoformat('2018-05-24T12:11:24.067')),
            ('SVF',
             'Sebastian Vettel',
             'FERRARI',
             datetime.datetime.fromisoformat('2018-05-24T12:02:58.917'),
             datetime.datetime.fromisoformat('2018-05-24T12:04:03.332')))),]

    # test get_datetime_info
    def test_get_datetime_info(self):
        """ Test get_datetime_info function."""
        for data in self.test_cases_datetime:
            m = mock_open(read_data=data[0])
            with patch("builtins.open", m):
                with open("test_file.txt", "r") as file:
                    assert code.get_datetime_info(file) == data[1]

    # test get_drivers_info
    def test_get_drivers_info(self):
        """ Test get_drivers_info function."""
        def class_for_test(case):
            object_t = code.Drivers(abbr=case[0],
                                     name=case[1],
                                     team=case[2],
                                     start_time=case[3],
                                     end_time=case[4])
            object_t.time = object_t.end_time - object_t.start_time
            if int(object_t.time.total_seconds()) < 0:
                object_t.error = 'incorrect data'
            return object_t

        for data in self.test_cases_driver:
            check_list = list()
            for item in data[1]:
                check_list.append(class_for_test(item))
            m = mock_open(read_data=data[0][0])
            with patch("builtins.open", m):
                with open("test_file.txt", "r") as file:
                    assert code.get_drivers_info(file, data[0][1], data[0][2]) == check_list
