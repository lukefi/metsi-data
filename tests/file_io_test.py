from dataclasses import dataclass
import os
import copy
import forestdatamodel.formats.file_io as fio
from tests.test_util import ConverterTestSuite, vmi13_stands

TEST_FILE = 'testfile'
absolute_resource_path = os.path.join(os.getcwd(), 'tests', 'resources')

@dataclass
class Test:
    a: int

    def __eq__(self, other):
        return self.a == other.a
class FileIoTest(ConverterTestSuite):

    def test_select_vmi_reader_and_read_vmi_file(self):
        reference_file = os.path.join(absolute_resource_path, 'VMI12_source_mini.dat')
        file_reader = fio.select_file_reader('vmi')
        input_data = file_reader(reference_file)
        result = len(input_data)
        self.assertEqual(result, 24)

    def test_select_xml_reader_and_read_xml_file(self):
        reference_file = os.path.join(absolute_resource_path, 'SMK_source.xml')
        file_reader = fio.select_file_reader('xml')
        input_data = file_reader(reference_file)
        result = len(input_data)
        self.assertEqual(result, 28715)

    def test_rsd_float(self):
        assertions = [
            ([123], "123.000000"),
            ([0], "0.000000"),
            ([123.4455667788], "123.445567"),
            ([None], "0.000000"),
            (["1.23"], "1.230000"),
            (["abc"], "0.000000")
        ]
        self.run_with_test_assertions(assertions, fio.rsd_float)

    def test_rsd_forest_stand_rows(self):
        result = fio.rsd_forest_stand_rows(vmi13_stands[0])
        self.assertEqual(3, len(result))

    def test_rsd_rows(self):
        result = fio.rsd_rows(vmi13_stands)
        self.assertEqual(5, len(result))

    def test_csv_rows(self):
        result = fio.csv_rows(vmi13_stands, ";")
        self.assertEqual(5, len(result))

    def test_write_forest_rsd(self):
        fio.write_forest_rsd(vmi13_stands, TEST_FILE)
        result = open(TEST_FILE, 'r', newline='\n').readlines()
        self.assertEqual(5, len(result))
        os.remove(TEST_FILE)

    def test_write_forest_csv(self):
        fio.write_forest_csv(vmi13_stands, TEST_FILE)
        result = open(TEST_FILE, 'r', newline='\n').readlines()
        self.assertEqual(5, len(result))
        os.remove(TEST_FILE)

    def test_generate_json_file(self):
        stands = copy.deepcopy(vmi13_stands)
        fio.write_forest_json(stands, TEST_FILE)
        self.assertEqual(os.path.exists(TEST_FILE), True)
        os.remove(TEST_FILE)

    
    def test_pickle(self):
        data = [
            Test(a=1),
            Test(a=2)
        ]
        fio.pickle_writer('testpickle', data)
        result = fio.pickle_reader('testpickle')
        self.assertListEqual(data, result)
        os.remove('testpickle')   

