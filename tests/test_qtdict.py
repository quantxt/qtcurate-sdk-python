from unittest import TestCase, main
import requests
from unittest.mock import patch, Mock
from qtcurate.qtdict import QtDict
from qtcurate.exceptions import *


API_KEY = 'some_key'


class TestQtDict(TestCase):

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

    @patch("qtcurate.qtdict.requests.Session")
    def test_list_empty(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 200
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        dic = QtDict(API_KEY)
        all_dictionaries = dic.list()
        self.assertEqual(all_dictionaries, [])

    @patch("qtcurate.qtdict.requests.Session")
    def test_list_non_empty(self, session):
        dicts = [
            {
                'id': 'b8c8421c-ee76-4b0a-a42f-1ab01de7217b',
                'key': 'mbjelanovic-gmail-com/b8c8421c-ee76-4b0a-a42f-1ab01de7217b.csv.gz',
                'name': 'some name',
                'global': False,
                'entries': []
            }
        ]

        mock = Mock()
        response = Mock()
        response.status_code = 200
        response.json.return_value = dicts
        mock.get.return_value = response
        session.return_value = mock

        dic = QtDict(API_KEY)
        all_dictionaries = dic.list()
        self.assertEqual(all_dictionaries, dicts)

    @patch("qtcurate.qtdict.requests.Session")
    def test_list_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        dic = QtDict(API_KEY)
        with self.assertRaises(QtRestApiError):
            dic.list()

    @patch("qtcurate.qtdict.requests.Session")
    def test_list_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict(API_KEY)
        with self.assertRaises(QtConnectionError):
            dic.list()

    def test_create_miss_name(self):
        entries = {"str": "str", "category": "category"}
        dic = QtDict(API_KEY)
        dic.entries(entries)
        with self.assertRaises(QtDictError):
            dic.create()

    def test_create_entry(self):
        name = "some name"
        dic = QtDict(API_KEY)
        dic.name(name)
        with self.assertRaises(QtDictError):
            dic.create()

    @patch("qtcurate.qtdict.requests.Session")
    def test_create_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock

        dic = QtDict(API_KEY)
        dic.name("test")
        test_dict = {"str": "str", "category": "category"}
        dic.entries(test_dict)
        with self.assertRaises(QtRestApiError):
            dic.create()

    @patch("qtcurate.qtdict.requests.Session")
    def test_create_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict(API_KEY)
        dic.name("test")
        test_dict = {"str": "str", "category": "category"}
        dic.entries(test_dict)
        with self.assertRaises(QtConnectionError):
            dic.create()

    @patch("qtcurate.qtdict.requests.Session")
    def test_create(self, session):
        temp_json = {'id': '21c317a7-1808-4fb2-976d-66faa35c445f',
                    'name': 'test', 'global': False,
                    'entries': [{'str': 'str', 'category': 'category'}]}
        mock = Mock()
        response = Mock()
        response.status_code = 200
        response.json.return_value = temp_json
        mock.post.return_value = response
        session.return_value = mock

        dic = QtDict(API_KEY)
        dic.name("test")
        test_dict = {"str": "str", "category": "category"}
        dic.entries(test_dict)
        self.assertEqual(dic.create(), temp_json)

    def test_fetch_arg(self):
        dict_id = 123
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.fetch(dict_id)

    @patch("qtcurate.qtdict.requests.Session")
    def test_fetch_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        dic = QtDict(API_KEY)
        with self.assertRaises(QtRestApiError):
            dic.fetch("some dictionar id")

    @patch("qtcurate.qtdict.requests.Session")
    def test_fetch_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict(API_KEY)
        with self.assertRaises(QtConnectionError):
            dic.fetch("some dictionary id")

    @patch("qtcurate.qtdict.requests.Session")
    def test_delete_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.delete.return_value = response
        session.return_value = mock

        dic = QtDict(API_KEY)
        with self.assertRaises(QtRestApiError):
            dic.delete("some dictionary id")

    @patch("qtcurate.qtdict.requests.Session")
    def test_delete_connection_exception(self, session):
        mock = Mock()
        mock.delete.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict(API_KEY)
        with self.assertRaises(QtConnectionError):
            dic.delete("some dictionar id")

    def test_delete_arg(self):
        dict_id = 123
        dic = QtDict(API_KEY)
        with self.assertRaises(QtArgumentError):
            dic.delete(dict_id)

    @patch("qtcurate.qtdict.requests.Session")
    def test_update_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.put.return_value = response
        session.return_value = mock

        dic = QtDict(API_KEY)
        dic.name("test")
        test_dict = {"str": "str", "category": "category"}
        dic.entries(test_dict)
        with self.assertRaises(QtRestApiError):
            dic.update("some dictionar id")

    @patch("qtcurate.qtdict.requests.Session")
    def test_update_connection_exception(self, session):
        mock = Mock()
        mock.put.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict(API_KEY)
        dic.name("test")
        test_dict = {"str": "str", "category": "category"}
        dic.entries(test_dict)
        with self.assertRaises(QtConnectionError):
            dic.update("some dictionar id")

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

    @patch("qtcurate.qtdict.requests.Session")
    def test_upload_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock
        dic = QtDict(API_KEY)
        file_path = "test.tsv"
        name = "test name"

        with self.assertRaises(QtRestApiError):
            dic.upload(file_path, name)

    @patch("qtcurate.qtdict.requests.Session")
    def test_upload_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict(API_KEY)
        file_path = "test.tsv"
        name = "test name"

        with self.assertRaises(QtConnectionError):
            dic.upload(file_path, name)

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
