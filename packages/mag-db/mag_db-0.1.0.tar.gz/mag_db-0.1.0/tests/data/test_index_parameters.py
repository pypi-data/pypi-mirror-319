import unittest
from datetime import date

from mag_db.data.index_parameters import IndexParameters


class TestIndexParameters(unittest.TestCase):
    def setUp(self):
        self.index_parameters = IndexParameters()

    def test_set_string(self):
        self.index_parameters.set_string("test")
        self.assertEqual(self.index_parameters.parameters, ["test"])
        self.assertEqual(len(self.index_parameters.type_handlers), 1)

    def test_set_int(self):
        self.index_parameters.set_int(123)
        self.assertEqual(self.index_parameters.parameters, [123])
        self.assertEqual(len(self.index_parameters.type_handlers), 1)

    def test_set_date(self):
        test_date = date(2023, 1, 1)
        self.index_parameters.set_date(test_date)
        self.assertEqual(self.index_parameters.parameters, [test_date])
        self.assertEqual(len(self.index_parameters.type_handlers), 1)

    def test_set_bean(self):
        class TestBean:
            def __init__(self, name, age):
                self.name = name
                self.age = age

        bean = TestBean("Alice", 30)
        self.index_parameters.set_bean(bean, ["name", "age"])
        self.assertEqual(self.index_parameters.parameters, ["Alice", 30])
        self.assertEqual(len(self.index_parameters.type_handlers), 2)

    def test_set_field_map(self):
        field_map = {"name": "Alice", "age": 30}
        self.index_parameters.set_field_map(field_map, ["name", "age"])
        self.assertEqual(self.index_parameters.parameters, ["Alice", 30])
        self.assertEqual(len(self.index_parameters.type_handlers), 2)

if __name__ == '__main__':
    unittest.main()
