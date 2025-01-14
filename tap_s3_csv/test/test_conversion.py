import unittest

from tap_s3_csv.conversion import count_sample, count_samples, \
    pick_datatype, generate_schema


class TestConverter(unittest.TestCase):

    def test_convert(self):
        # none
        self.assertEqual(convert(''), (None, None,))
        self.assertEqual(convert(None), (None, None,))

        # integers
        self.assertEqual(convert('1'), (1, 'integer',))
        self.assertEqual(convert('-1'), (-1, 'integer',))

        # floats
        self.assertEqual(convert('1.0'), (1.0, 'number',))

        # dates
        self.assertEqual(convert('2017-01-01'),
                         ('2017-01-01', 'string'))
        self.assertEqual(convert('2017-01-01', 'date-time'),
                         ('2017-01-01T00:00:00+00:00', 'date-time'))

        self.assertEqual(convert('2017-01-01T01:01:01+04:00'),
                         ('2017-01-01T01:01:01+04:00', 'string'))
        self.assertEqual(convert('2017-01-01T01:01:01+04:00', 'date-time'),
                         ('2017-01-01T01:01:01+04:00', 'date-time'))

        self.assertEqual(convert('2017-01-01T01:01'),
                         ('2017-01-01T01:01', 'string'))
        self.assertEqual(convert('2017-01-01T01:01', 'date-time'),
                         ('2017-01-01T01:01:00+00:00', 'date-time'))

        # strings
        self.assertEqual(convert('4 o clock'), ('4 o clock', 'string'))

    def test_count_sample(self):
        self.assertEqual(
            count_sample({'id': '1', 'first_name': 'Connor'}),
            {'id': {'integer': 1}, 'first_name': {'string': 1}})

    def test_count_samples(self):
        self.assertEqual(
            count_samples([{'id': '1', 'first_name': 'Connor'},
                           {'id': '2', 'first_name': '1'}]),
            {'id': {'integer': 2}, 'first_name': {'string': 1,
                                                  'integer': 1}})

    def test_pick_datatype(self):
        self.assertEqual(pick_datatype({'string': 1}), 'string')
        self.assertEqual(pick_datatype({'integer': 1}), 'integer')
        self.assertEqual(pick_datatype({'number': 1}), 'number')

        self.assertEqual(pick_datatype({'number': 1,
                                        'integer': 1}), 'number')

        self.assertEqual(pick_datatype({'string': 1,
                                        'integer': 1}), 'string')
        self.assertEqual(pick_datatype({'string': 1,
                                        'number': 1}), 'string')
        self.assertEqual(pick_datatype({}), 'string')

    def test_generate_schema(self):
        self.assertEqual(
            generate_schema([{'id': '1', 'first_name': 'Connor'},
                             {'id': '2', 'first_name': '1'}]),
            {'id': {'type': ['null', 'integer'],
                    '_conversion_type': 'integer'},
             'first_name': {'type': ['null', 'string'],
                            '_conversion_type': 'string'}})

        self.assertEqual(
            generate_schema([{'id': '1', 'cost': '1'},
                             {'id': '2', 'cost': '1.25'}]),
            {'id': {'type': ['null', 'integer'],
                    '_conversion_type': 'integer'},
             'cost': {'type': ['null', 'number'],
                      '_conversion_type': 'number'}})

        self.assertEqual(
            generate_schema([{'id': '1', 'date': '2017-01-01'},
                             {'id': '2', 'date': '2017-01-02'}]),
            {'id': {'type': ['null', 'integer'],
                    '_conversion_type': 'integer'},
             'date': {'type': ['null', 'string'],
                      '_conversion_type': 'string'}})
