import unittest
import os
from forestdatamodel.cli import conv_read

# We assert that the workdir for launching this test suite is 'src' for module resolution
# We need to use absolute path for Windows compatibility
absolute_resource_path = os.path.join(os.getcwd(), 'tests', 'resources')

class TestForestBuilderRun(unittest.TestCase):

    def test_run_smk_forest_builder_build(self):
        assertion = (('SMK_source.xml', 'forest_centre'), 3)
        reference_file = os.path.join(absolute_resource_path, assertion[0][0])
        list_of_stands = conv_read(reference_file, assertion[0][1], {"strata_origin": "1", "reference_trees": False})
        result = len(list_of_stands)
        self.assertEqual(result, assertion[1])


    def test_run_vmi12_forest_builder_build(self):
        assertion = (('VMI12_source_mini.dat', 'vmi12'), 7)
        reference_file = os.path.join(absolute_resource_path, assertion[0][0])
        list_of_stands = conv_read(reference_file, assertion[0][1], {"reference_trees": False})
        result = len(list_of_stands)
        self.assertEqual(result, assertion[1])


    def test_run_vmi13_forest_builder_build(self):
        assertion = (('VMI13_source_mini.dat', 'vmi13'), 3)
        reference_file = os.path.join(absolute_resource_path, assertion[0][0])
        list_of_stands = conv_read(reference_file, assertion[0][1], {"reference_trees": False})
        result = len(list_of_stands)
        self.assertEqual(result, assertion[1])
