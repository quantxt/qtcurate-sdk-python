from qtcurate.result import Field, FieldValue, Result, Position
from unittest import TestCase, main
from unittest.mock import Mock, patch
from qtcurate.exceptions import *


category = "category"
vocab_name = "dict_name"
vocab_id = "dict_id"
type_field = "type"
str_field = "str"
double_value = "doubleValue"
int_value = "intValue"
datetime_value = "datetimeValue"


class TestResult(TestCase):

    # ***************************************************
    # Testing Position class
    # ***************************************************
    def test_set_start(self):
        position = Position()
        some_val = 123
        position.set_start(some_val)
        self.assertEqual(position.start, some_val)

    def test_get_start(self):
        position = Position()
        self.assertEqual(position.get_start(), None)
    # ***************************************************
    # Testing FieldValue class
    # ***************************************************

    def test_field_value_set_str(self):
        fv = FieldValue()
        some_val = '123'
        fv.set_str(some_val)
        self.assertEqual(fv.str_value, some_val)

    def test_field_value_get_str(self):
        fv = FieldValue()
        self.assertEqual(fv.get_str(), None)




    # ***************************************************
    # Testing Field
    # ***************************************************

    def test_field_set_values(self):
        field = Field()
        some_val = [1, 2, 3]
        field.set_values(some_val)
        self.assertEqual(field.values, some_val)

    def test_field_get_values(self):
        field = Field()
        self.assertEqual(field.get_values(), None)

    def test_field_set_str(self):
        field = Field()
        some_val = '123'
        field.set_str(some_val)
        self.assertEqual(field.str, some_val)

    def test_field_set_type(self):
        field = Field()
        some_val = '123'
        field.set_type(some_val)
        self.assertEqual(field.type, some_val)

    def test_field_set_vocab_name(self):
        field = Field()
        some_val = '123'
        field.set_vocab_name(some_val)
        self.assertEqual(field.vocab_name, some_val)

    def test_field_set_category(self):
        field = Field()
        some_val = '123'
        field.set_category(some_val)
        self.assertEqual(field.category, some_val)

    def test_field_set_vocab_id(self):
        field = Field()
        some_val = '123'
        field.set_vocab_id(some_val)
        self.assertEqual(field.vocab_id, some_val)

    def test_field_get_vocab_id(self):
        field = Field()
        self.assertEqual(field.get_vocab_id(), None)

    def test_field_get_vocab_name(self):
        field = Field()
        self.assertEqual(field.get_vocab_name(), None)

    def test_field_get_category(self):
        field = Field()
        self.assertEqual(field.get_category(), None)

    def test_field_get_str(self):
        field = Field()
        self.assertEqual(field.get_str(), None)

    def test_field_get_type(self):
        field = Field()
        self.assertEqual(field.get_type(), None)

    # ***************************************************
    # Testing Result
    # ***************************************************

    # Test raw_exporter method
    def test_result_raw_exporter_arg_err(self):
        some_id = 'some id'
        result = Result(some_id)
        with self.assertRaises(QtArgumentError):
            result.raw_exporter([1, 2, 3])

    def test_result_raw_exporter_no_permission(self):
        path = "/usr/bin/path.txt"
        some_id = 'some id'
        result = Result(some_id)
        with self.assertRaises(QtArgumentError):
            result.raw_exporter(path)

    def test_result_raw_exporter_no_json(self):
        path = "path.tsv"
        some_id = 'some id'
        result = Result(some_id)
        with self.assertRaises(QtFileTypeError):
            result.raw_exporter(path)

    @patch("qtcurate.result.connect")
    def test_result_raw_exporter(self, con):
        pass

    # Test result_xlsx_exporter method
    def test_result_xlsx_exporter_arg_err(self):
        some_id = 'some id'
        result = Result(some_id)
        with self.assertRaises(QtArgumentError):
            result.result_xlsx_exporter([1, 2, 3])

    def test_result_xlsx_exporter_no_permission(self):
        path = "/usr/bin/path.txt"
        some_id = 'some id'
        result = Result(some_id)
        with self.assertRaises(QtArgumentError):
            result.result_xlsx_exporter(path)

    def test_result_xlsx_exporter_no_xlsx(self):
        path = "path.txt"
        some_id = 'some id'
        result = Result(some_id)
        with self.assertRaises(QtFileTypeError):
            result.result_xlsx_exporter(path)

    @patch("qtcurate.result.connect")
    def test_result_xlsx_exporter(self, con):
        pass

    # Test read method
    @patch("qtcurate.result.connect")
    def test_read(self, con):
        some_id = 'some id'
        some_dict = {"key": "value"}
        result = Result(some_id)
        response = Mock()
        response.json.return_value = some_dict
        con.return_value = response
        res = result.read()
        self.assertEqual(res, [])


if __name__ == '__main__':
    main()
