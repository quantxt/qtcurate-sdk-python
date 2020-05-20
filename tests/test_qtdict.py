from unittest import TestCase, main
import requests
from unittest.mock import patch, Mock
from qtcurate.qtdict import QtDict
from qtcurate.exceptions import *


class TestQtDict(TestCase):

    def test_name_name(self):
        name = "some name"
        dic = QtDict('123456')
        dic.name(name)
        self.assertEqual(name, dic.temp_dict["name"])

    def test_name_type(self):
        name = 12345
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.name(name)

    def test_entries_type(self):
        test_dict = "string"
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.entries(test_dict)

    def test_entries_dict_len(self):
        test_dict = {"key": "key"}
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.entries(test_dict)

    def test_entries_dict_content(self):
        test_dict = {"key": "key", "test": "value"}
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.entries(test_dict)

    def test_entries(self):
        test_dict = {"key": "key", "value": "value"}
        dic = QtDict('1234567')
        dic.entries(test_dict)
        self.assertEqual([test_dict], dic.temp_dict['entries'])

    def test_add_entry(self):
        key = "New York"
        value = "Knicks"
        list_entries = [{"key": key, "value": value}]
        dic = QtDict('123456')
        dic.add_entry(key, value)
        self.assertEqual(list_entries, dic.temp_dict['entries'])

    def test_add_entry_key_type(self):
        key = ["test"]
        value = "Knicks"
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.add_entry(key, value)

    def test_add_entry_value_type(self):
        key = "test"
        value = ["Knicks"]
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.add_entry(key, value)

    @patch("qtcurate.qtdict.requests.Session")
    def test_list_empty(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 200
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        dic = QtDict('123456')
        all_dictionaries = dic.list()
        assert all_dictionaries == []

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

        dic = QtDict('123456')
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

        dic = QtDict('123456')
        self.assertRaises(QtRestApiError, dic.list)

    @patch("qtcurate.qtdict.requests.Session")
    def test_list_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict('123456')
        self.assertRaises(QtConnectionError, dic.list)

    def test_create_miss_name(self):
        entries = {"key": "key", "value": "value"}
        dic = QtDict('123456')
        dic.entries(entries)
        with self.assertRaises(QtDictError):
            dic.create()

    def test_create_entry(self):
        name = "some name"
        dic = QtDict('123456')
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

        dic = QtDict('123456')
        dic.name("test")
        test_dict = {"key": "key", "value": "value"}
        dic.entries(test_dict)

        self.assertRaises(QtRestApiError, dic.create)

    @patch("qtcurate.qtdict.requests.Session")
    def test_create_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict('123456')
        dic.name("test")
        test_dict = {"key": "key", "value": "value"}
        dic.entries(test_dict)

        self.assertRaises(QtConnectionError, dic.create)

    def test_fetch_arg(self):
        dict_id = 123
        dic = QtDict('123456')
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

        dic = QtDict('123456')
        with self.assertRaises(QtRestApiError):
            dic.fetch("some dictionar id")

    @patch("qtcurate.qtdict.requests.Session")
    def test_fetch_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict('123456')
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

        dic = QtDict('123456')
        with self.assertRaises(QtRestApiError):
            dic.delete("some dictionary id")

    @patch("qtcurate.qtdict.requests.Session")
    def test_delete_connection_exception(self, session):
        mock = Mock()
        mock.delete.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict('123456')
        with self.assertRaises(QtConnectionError):
            dic.delete("some dictionar id")

    def test_delete_arg(self):
        dict_id = 123
        dic = QtDict('123456')
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

        dic = QtDict('123456')
        dic.name("test")
        test_dict = {"key": "key", "value": "value"}
        dic.entries(test_dict)
        with self.assertRaises(QtRestApiError):
            dic.update("some dictionar id")

    @patch("qtcurate.qtdict.requests.Session")
    def test_update_connection_exception(self, session):
        mock = Mock()
        mock.put.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict('123456')
        dic.name("test")
        test_dict = {"key": "key", "value": "value"}
        dic.entries(test_dict)
        with self.assertRaises(QtConnectionError):
            dic.update("some dictionar id")

    def test_update_arg_type(self):
        dict_id = 123
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.update(dict_id)

    def test_update_name(self):
        dict_id = "string"
        entries = {"key": "key", "value": "value"}
        dic = QtDict('123456')
        dic.entries(entries)
        with self.assertRaises(QtDictError):
            dic.update(dict_id)

    def test_update_entries(self):
        dict_id = "string"
        name = "name"
        dic = QtDict('123456')
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
        dic = QtDict('123456')
        file_path = "test.tsv"
        name = "test name"

        with self.assertRaises(QtRestApiError):
            dic.upload(file_path, name)

    @patch("qtcurate.qtdict.requests.Session")
    def test_upload_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = QtDict('123456')
        file_path = "test.tsv"
        name = "test name"

        with self.assertRaises(QtConnectionError):
            dic.upload(file_path, name)

    def test_upload_arg_name_type(self):
        file = 123
        name = "name"
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.upload(file, name)

    def test_upload_arg_path_type(self):
        file = "path"
        name = 123
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.upload(file, name)

    def test_upload_file_type(self):
        file = "path"
        name = "name"
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.upload(file, name)

    def test_upload_file_exist(self):
        file = "path.tsv"
        name = "name"
        dic = QtDict('123456')
        with self.assertRaises(QtArgumentError):
            dic.upload(file, name)

if __name__ == '__main__':
    main()
