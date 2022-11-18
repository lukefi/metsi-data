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

    def test_stands_to_csv(self):
        delimiter = ";"
        result = fio.stands_to_csv(vmi13_stands, delimiter)
        self.assertEqual(6, len(result))
        
        #make sure that each type of a row has the same number of columns, since csv-->stand conversion relies on it
        stand_row_lengths = [len(row.split(delimiter)) for row in result if row[0:5] == "stand"]
        tree_row_lengths = [len(row.split(delimiter)) for row in result if row[0:4] == "tree"]
        stratum_rows_lengths = [len(row.split(delimiter)) for row in result if row[0:7] == "stratum"]

        self.assertTrue(all(length==stand_row_lengths[0] for length in stand_row_lengths))
        self.assertTrue(all(length==tree_row_lengths[0] for length in tree_row_lengths))
        self.assertTrue(all(length==stratum_rows_lengths[0] for length in stratum_rows_lengths))

    def test_csv_to_stands(self):
        """tests that the roundtrip conversion stands-->csv-->stands maintains the stand structure"""
        delimiter = ";"
        result = fio.stands_to_csv(vmi13_stands, delimiter)
        path = "tests/resources/vmi13_stands.csv"
        with open(path, "w") as file: 
            file.write("\n".join(result))

        stands_from_csv = fio.csv_to_stands(path, delimiter)
        self.assertEqual(2, len(stands_from_csv))
        os.remove(path)

        # Test that the stands from csv and the original stands are equal.
        # It performs a sort of "deep diff" for the stands, relying on the fact that only reference_trees and tree_strata are nested objects in the stand.
        # Objects are cast to dicts to avoid using the overridden __eq__ methods of the respective classes.
        for i in range(len(vmi13_stands)):
            for t in range(len(vmi13_stands[i].reference_trees)):
                trees_expected = vmi13_stands[i].reference_trees[t].__dict__
                trees_actual = stands_from_csv[i].reference_trees[t].__dict__
                self.assertTrue(trees_expected == trees_actual)
            
            for s in range(len(vmi13_stands[i].tree_strata)):
                strata_expected = vmi13_stands[i].tree_strata[s].__dict__
                strata_actual = stands_from_csv[i].tree_strata[s].__dict__
                self.assertTrue(strata_expected == strata_actual)

            stands_expected = vmi13_stands[i].__dict__
            stands_actual = stands_from_csv[i].__dict__
            self.assertTrue(stands_expected == stands_actual)


    def test_write_forest_rsd(self):
        fio.write_forest_rsd(vmi13_stands, TEST_FILE)
        result = open(TEST_FILE, 'r', newline='\n').readlines()
        self.assertEqual(5, len(result))
        os.remove(TEST_FILE)

    def test_write_forest_csv(self):
        fio.write_forest_csv(vmi13_stands, TEST_FILE)
        result = open(TEST_FILE, 'r', newline='\n').readlines()
        self.assertEqual(6, len(result))
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

