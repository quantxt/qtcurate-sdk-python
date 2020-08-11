from unittest import TestCase, main
from qtcurate.qtdict import QtDict
from qtcurate.exceptions import *


API_KEY = 'a5334f7d-2aac-44b3-aefc-a25cd9dd7bec'


class TestQtDict(TestCase):

    def test_get_id(self):
        dic = QtDict(API_KEY)
        some_id = None
        self.assertEqual(dic.get_id(), str(some_id))

    def test_name_name(self):
        name = "some name"
        dic = QtDict(API_KEY)
        dic.name(name)
        self.assertEqual(name, dic.temp_dict["name"])

    def test_name_type(self):
        name = 12345
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.name(name)

    def test_entries_type(self):
        test_dict = "string"
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.entries(test_dict)

    def test_entries_dict_len_3(self):
        test_dict = {"str": "str", "category": "category", "some_key": "some_value"}
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.entries(test_dict)

    def test_entries_dict_len_0(self):
        test_dict = {}
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.entries(test_dict)

    def test_entries_dict_content(self):
        test_dict = {"test": "str", "category": "category"}
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.entries(test_dict)

    def test_entries_dict_content_2(self):
        test_dict = {"str": "str", "test": "category"}
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.entries(test_dict)

    def test_entries(self):
        test_dict = {"str": "str", "category": "category"}
        dic = QtDict(API_KEY)
        dic.entries(test_dict)
        self.assertEqual([test_dict], dic.temp_dict['entries'])

    def test_entries_1(self):
        test_dict = {"str": "str"}
        dic = QtDict(API_KEY)
        dic.entries(test_dict)
        self.assertEqual([test_dict], dic.temp_dict['entries'])

    def test_add_entry(self):
        key = "New York"
        value = "Knicks"
        list_entries = [{"str": key, "category": value}]
        dic = QtDict(API_KEY)
        dic.add_entry(key, value)
        self.assertEqual(list_entries, dic.temp_dict['entries'])

    def test_add_entry_key_type(self):
        key = ["test"]
        value = "Knicks"
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.add_entry(key, value)

    def test_add_entry_value_type(self):
        key = "test"
        value = ["Knicks"]
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.add_entry(key, value)

    def test_add_entry_value_none(self):
        key = "test"
        value = None
        list_entries = [{"str": key}]
        dic = QtDict(API_KEY)
        dic.add_entry(key, value)
        self.assertEqual(list_entries, dic.temp_dict['entries'])

    # def test_list????

    def test_fetch_arg(self):
        dict_id = 123
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.fetch(dict_id)

    def test_delete_arg(self):
        dict_id = 123
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.delete(dict_id)

    def test_create_miss_name(self):
        entries = {"str": "str", "category": "category"}
        dic = QtDict(API_KEY)
        dic.entries(entries)
        with self.assertRaises(QtDictError):
            dic.create()

    def test_create_miss_entry(self):
        name = "some name"
        dic = QtDict(API_KEY)
        dic.name(name)
        with self.assertRaises(QtDictError):
            dic.create()

    def test_update_arg_type(self):
        dict_id = 123
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.update(dict_id)

    def test_update_name(self):
        dict_id = "string"
        entries = {"str": "str", "category": "category"}
        dic = QtDict(API_KEY)
        dic.entries(entries)
        with self.assertRaises(QtDictError):
            dic.update(dict_id)

    def test_update_entries(self):
        dict_id = "string"
        name = "name"
        dic = QtDict(API_KEY)
        dic.name(name)
        with self.assertRaises(QtDictError):
            dic.update(dict_id)

    def test_upload_arg_file_type(self):
        file = 123
        name = "name"
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.upload(file, name)

    def test_upload_arg_name_type(self):
        file = "path"
        name = 123
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.upload(file, name)

    def test_upload_file_extension(self):
        file = "path"
        name = "name"
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.upload(file, name)

    def test_upload_file_exist(self):
        file = "path.tsv"
        name = "name"
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.upload(file, name)


if __name__ == '__main__':
    main()
