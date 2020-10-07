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
    # Test set_start method
    def test_position_set_start_arg_err(self):
        position = Position()
        some_val = 'some val'
        with self.assertRaises(QtArgumentError):
            position.set_start(some_val)

    def test_position_set_start(self):
        position = Position()
        some_val = 123
        position.set_start(some_val)
        self.assertEqual(position.start, some_val)

    # Test get_start method
    def test_position_get_start(self):
        position = Position()
        self.assertEqual(position.get_start(), None)

    # Test set_end method
    def test_position_set_end_arg_err(self):
        position = Position()
        some_val = 'some val'
        with self.assertRaises(QtArgumentError):
            position.set_end(some_val)

    def test_position_set_end(self):
        position = Position()
        some_val = 123
        position.set_end(some_val)
        self.assertEqual(position.end, some_val)

    # Test get_start method
    def test_position_get_end(self):
        position = Position()
        self.assertEqual(position.get_end(), None)

    # Test set_line method
    def test_position_set_line_arg_err(self):
        position = Position()
        some_val = 'some val'
        with self.assertRaises(QtArgumentError):
            position.set_line(some_val)

    def test_position_set_line(self):
        position = Position()
        some_val = 123
        position.set_line(some_val)
        self.assertEqual(position.line, some_val)

    # Test get_int method
    def test_position_get_int_value(self):
        position = Position()
        self.assertEqual(position.get_int_value(), None)

    # ***************************************************
    # Testing FieldValue class
    # ***************************************************
    # Test set_str method
    def test_field_value_set_str_arg_err(self):
        fv = FieldValue()
        some_val = 123
        with self.assertRaises(QtArgumentError):
            fv.set_str(some_val)

    def test_field_value_set_str(self):
        fv = FieldValue()
        some_val = '123'
        fv.set_str(some_val)
        self.assertEqual(fv.str_value, some_val)
    # Test get_str method
    def test_field_value_get_str(self):
        fv = FieldValue()
        self.assertEqual(fv.get_str(), None)

    # ***************************************************
    # Testing Field class
    # ***************************************************
    # Test set_value method
    def test_field_set_values_arg_err(self):
        field = Field()
        some_val = 123
        with self.assertRaises(QtArgumentError):
            field.set_values(some_val)

    def test_field_set_values(self):
        field = Field()
        some_val = [1, 2, 3]
        field.set_values(some_val)
        self.assertEqual(field.values, some_val)

    # Test get_str method
    def test_field_get_values(self):
        field = Field()
        self.assertEqual(field.get_values(), None)

    # Test set_str method
    def test_field_set_str_arg_err(self):
        field = Field()
        some_val = 123
        with self.assertRaises(QtArgumentError):
            field.set_str(some_val)

    def test_field_set_str(self):
        field = Field()
        some_val = '123'
        field.set_str(some_val)
        self.assertEqual(field.str, some_val)

    # Test get_str method
    def test_get_str(self):
        field = Field()
        self.assertEqual(field.get_str(), None)

    # Test set_type method
    def test_field_set_type_arg_err(self):
        field = Field()
        some_val = 123
        with self.assertRaises(QtArgumentError):
            field.set_type(some_val)

    def test_field_set_type(self):
        field = Field()
        some_val = '123'
        field.set_type(some_val)
        self.assertEqual(field.type, some_val)

    # Test get_type method
    def test_get_type(self):
        field = Field()
        self.assertEqual(field.get_type(), None)

    # Test set_vocab_name method
    def test_field_set_vocab_name_arg_err(self):
        field = Field()
        some_val = 123
        with self.assertRaises(QtArgumentError):
            field.set_vocab_name(some_val)

    def test_field_set_vocab_name(self):
        field = Field()
        some_val = '123'
        field.set_vocab_name(some_val)
        self.assertEqual(field.vocab_name, some_val)

    # Test get_vocab_name method
    def test_get_vocab_name(self):
        field = Field()
        self.assertEqual(field.get_vocab_name(), None)

    # Test set_category method
    def test_field_set_category_arg_err(self):
        field = Field()
        some_val = 123
        with self.assertRaises(QtArgumentError):
            field.set_category(some_val)

    def test_field_set_category(self):
        field = Field()
        some_val = '123'
        field.set_category(some_val)
        self.assertEqual(field.category, some_val)

    # Test get_category method
    def test_field_get_category(self):
        field = Field()
        self.assertEqual(field.get_category(), None)

    # Test set_vocab_id method
    def test_field_set_vocab_id_arg_err(self):
        field = Field()
        some_val = 123
        with self.assertRaises(QtArgumentError):
            field.set_vocab_id(some_val)

    def test_field_set_vocab_id(self):
        field = Field()
        some_val = '123'
        field.set_vocab_id(some_val)
        self.assertEqual(field.vocab_id, some_val)

    # Test get_vocab_id method
    def test_field_get_vocab_id(self):
        field = Field()
        self.assertEqual(field.get_vocab_id(), None)

    # Test set_position method
    def test_field_set_position_arg_err(self):
        field = Field()
        some_val = 123
        with self.assertRaises(QtArgumentError):
            field.set_position(some_val)

    def test_set_position(self):
        field = Field()
        position = Position()
        field.set_position(position)
        self.assertEqual(field.position, position)

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
