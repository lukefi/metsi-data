import unittest
from dataclasses import dataclass

from lukefi.metsi.data.soa import Soa


@dataclass
class ExampleType(object):
    identifier: int = 1
    i: int = 1
    f: float = 1.0
    s: str = "1"

    def __hash__(self):
        return self.identifier


def create_fixture() -> list[ExampleType]:
    return [
        ExampleType(identifier=1),
        ExampleType(identifier=2),
        ExampleType(identifier=3)
    ]


class SoaTest(unittest.TestCase):
    def test_soa_initialization_with_no_properties(self):
        fixture = create_fixture()
        soa = Soa(fixture)
        self.assertEqual(3, len(soa.frame.columns))
        self.assertEqual(0, len(soa.frame.index))
        for f in fixture:
            self.assertTrue(soa.has_object(f))
            self.assertFalse(soa.has_object(ExampleType(identifier=4)))
            self.assertEqual(0, len(soa.frame[f]))

    def test_soa_initialization_with_some_properties(self):
        fixture = create_fixture()
        property_names = ['f', 'i']
        soa = Soa(fixture, property_names)
        self.assertEqual(3, len(soa.frame.columns))
        self.assertEqual(2, len(soa.frame.index))
        for prop in property_names:
            self.assertTrue(soa.has_property(prop))
        for f in fixture:
            self.assertTrue(soa.has_object(f))
            self.assertFalse(soa.has_object(ExampleType(identifier=4)))
            self.assertEqual(2, len(soa.frame[f]))
            self.assertListEqual([f.f, f.i], list(soa.frame[f]))

    def test_object_add_with_no_properties(self):
        fixture = create_fixture()
        soa = Soa(fixture)
        new_object_1 = ExampleType(identifier=4)
        new_object_2 = ExampleType(identifier=5)
        soa.upsert_objects([new_object_1, new_object_2])
        self.assertTrue(soa.has_object(new_object_1))
        self.assertTrue(soa.has_object(new_object_2))
        self.assertEqual(0, len(soa.frame[new_object_1]))
        self.assertEqual(0, len(soa.frame[new_object_2]))

    def test_new_object_upsert_with_some_properties(self):
        fixture = create_fixture()
        soa = Soa(fixture, ['i', 'f'])
        new_object_1 = ExampleType(identifier=4, i=4, f=4.0)
        fixture.append(new_object_1)
        new_object_2 = ExampleType(identifier=5, i=5, f=5.0)
        fixture.append(new_object_2)
        soa.upsert_objects([new_object_1, new_object_2])
        self.assertTrue(soa.has_object(new_object_1))
        self.assertTrue(soa.has_object(new_object_2))
        self.assertEqual(2, len(soa.frame[new_object_1]))
        self.assertEqual(2, len(soa.frame[new_object_2]))

        # column values
        self.assertListEqual([new_object_1.i, new_object_1.f], list(soa.frame[new_object_1]))
        self.assertListEqual([new_object_2.i, new_object_2.f], list(soa.frame[new_object_2]))

        # row values
        self.assertListEqual([x.i for x in fixture], list(soa.get_property_values('i')))
        self.assertListEqual([x.f for x in fixture], list(soa.get_property_values('f')))

    def test_existing_object_upsert_with_some_properties(self):
        fixture = create_fixture()
        soa = Soa(fixture, ['i', 'f'])
        new_value = 10
        fixture[0].i = new_value
        self.assertEqual([1, 1.0], list(soa.frame[fixture[0]]))
        soa.upsert_objects([fixture[0]])
        self.assertEqual([new_value, 1.0], list(soa.frame[fixture[0]]))

    def test_del_objects(self):
        fixture = create_fixture()
        soa = Soa(fixture)
        soa.del_objects([fixture[1]])
        self.assertEqual(2, len(soa.frame.columns))
        self.assertTrue(soa.has_object(fixture[0]))
        self.assertFalse(soa.has_object(fixture[1]))
        self.assertTrue(soa.has_object(fixture[2]))

    def test_get_object_properties(self):
        fixture = create_fixture()
        soa = Soa(fixture, ['i', 'f'])
        result = soa.get_object_properties(fixture[0])
        self.assertListEqual(['i', 'f'], [x[0] for x in result])
        self.assertListEqual([fixture[0].i, fixture[0].f], [x[1] for x in result])

    def test_get_existing_object_property(self):
        fixture = create_fixture()
        soa = Soa(fixture, ['i', 'f'])
        result = soa.get_object_property('i', fixture[0])
        self.assertEqual(1, result)

    def test_get_nonexisting_object_property(self):
        fixture = create_fixture()
        soa = Soa(fixture, ['i', 'f'])
        no_result_prop = soa.get_object_property('h', fixture[0])
        no_result_obj = soa.get_object_property('i', ExampleType(identifier=6))
        self.assertIsNone(no_result_prop)
        self.assertIsNone(no_result_obj)

    def test_get_property_values(self):
        fixture = create_fixture()
        soa = Soa(fixture, ['i', 'f'])
        result = soa.get_property_values('i')
        self.assertListEqual([x.i for x in fixture], list(result))

    def test_set_property_values(self):
        fixture = create_fixture()
        soa = Soa(fixture, ['i', 'f'])
        new_values = [3, 4, 5]
        soa.upsert_property_values('i', new_values)
        # TODO: should we prevent adding values for a property which does not exist in the base class?
        soa.upsert_property_values('g', new_values)

        self.assertListEqual([x.f for x in fixture], list(soa.get_property_values('f')))
        self.assertListEqual(new_values, list(soa.get_property_values('i')))
        self.assertListEqual(new_values, list(soa.get_property_values('g')))

        # should fail upon mismatch of row length
        self.assertRaises(ValueError, soa.upsert_property_values, *['i', [3, 4, 5, 6]])

