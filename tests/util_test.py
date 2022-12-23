from tests import test_util
from forestdatamodel.formats.util import multifilter, parse_int, parse_float, get_or_default


class TestOptionUtil(test_util.ConverterTestSuite):
    def test_parse_int(self):
        assertions = [
            (['123'], 123),
            ([' 2'], 2),
            ([' '], None),
            (['kissa123'], None),
        ]
        self.run_with_test_assertions(assertions, parse_int)

    def test_parse_float(self):
        assertions = [
            (['123'], 123.0),
            (['123.231'], 123.231),
            ([' 2'], 2.0),
            ([' '], None),
            (['kissa123'], None),
        ]
        self.run_with_test_assertions(assertions, parse_float)

    def test_get_or_default(self):
        assertions = [
            ([1], 1),
            ([None, 1], 1),
            ([None], None),
            ([None, None], None)
        ]
        self.run_with_test_assertions(assertions, get_or_default)

    def test_multifilter(self):
        def filter1(x: int) -> bool:
            return x > 10

        def filter2(x: int) -> bool:
            return x < 50

        result = multifilter([5, 10, 20, 40, 50, 55], filter1, filter2)
        self.assertEqual([20, 40], result)
