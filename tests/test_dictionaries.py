from unittest import TestCase
import requests
from unittest.mock import patch, Mock

from qt.dictionaries import Dictionary
from qt.exceptions import *


class TestDictionaries(TestCase):

    def test_name(self):
        name = "some name"
        dic = Dictionary('123456')
        dic.name(name)
        self.assertEqual(name, dic.d["name"])

    def test_entries(self):
        test_dict = {'key': "New York", "value": "Knicks"}
        dic = Dictionary('1234567')
        dic.entries(test_dict)
        self.assertEqual([test_dict], dic.d['entries'])

    def test_add_entry(self):
        key = "New York"
        value = "Knicks"
        list_entries = [{"key": key, "value": value}]
        dic = Dictionary('123456')
        dic.add_entry(key, value)
        self.assertEqual(list_entries, dic.d['entries'])

    @patch("qt.dictionaries.requests.Session")
    def test_list_empty(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 200
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        dic = Dictionary('123456')
        all_dictionaries = dic.list()
        assert all_dictionaries == []

    @patch("qt.dictionaries.requests.Session")
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

        dic = Dictionary('123456')
        all_dictionaries = dic.list()
        self.assertEqual(all_dictionaries, dicts)

    @patch("qt.dictionaries.requests.Session")
    def test_list_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        dic = Dictionary('123456')
        self.assertRaises(QTRestApiError, dic.list)

    @patch("qt.dictionaries.requests.Session")
    def test_list_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = Dictionary('123456')
        self.assertRaises(QTConnectionError, dic.list)

    @patch("qt.dictionaries.requests.Session")
    def test_create_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock

        dic = Dictionary('123456')
        dic.name("test")
        test_dict = {"key": "key", "value": "value"}
        dic.entries(test_dict)

        self.assertRaises(QTRestApiError, dic.create)

    @patch("qt.dictionaries.requests.Session")
    def test_create_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = Dictionary('123456')
        dic.name("test")
        test_dict = {"key": "key", "value": "value"}
        dic.entries(test_dict)

        self.assertRaises(QTConnectionError, dic.create)

    @patch("qt.dictionaries.requests.Session")
    def test_fetch_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        dic = Dictionary('123456')
        with self.assertRaises(QTRestApiError):
            dic.fetch("some dictionar id")

    @patch("qt.dictionaries.requests.Session")
    def test_fetch_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = Dictionary('123456')
        with self.assertRaises(QTConnectionError):
            dic.fetch("some dictionary id")

    @patch("qt.dictionaries.requests.Session")
    def test_delete_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.delete.return_value = response
        session.return_value = mock

        dic = Dictionary('123456')
        with self.assertRaises(QTRestApiError):
            dic.delete("some dictionary id")

    @patch("qt.dictionaries.requests.Session")
    def test_delete_connection_exception(self, session):
        mock = Mock()
        mock.delete.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = Dictionary('123456')
        with self.assertRaises(QTConnectionError):
            dic.delete("some dictionar id")

    @patch("qt.dictionaries.requests.Session")
    def test_update_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.put.return_value = response
        session.return_value = mock

        dic = Dictionary('123456')
        dic.name("test")
        test_dict = {"key": "key", "value": "value"}
        dic.entries(test_dict)
        with self.assertRaises(QTRestApiError):
            dic.update("some dictionar id")

    @patch("qt.dictionaries.requests.Session")
    def test_update_connection_exception(self, session):
        mock = Mock()
        mock.put.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = Dictionary('123456')
        dic.name("test")
        test_dict = {"key": "key", "value": "value"}
        dic.entries(test_dict)
        with self.assertRaises(QTConnectionError):
            dic.update("some dictionar id")

    @patch("qt.dictionaries.requests.Session")
    def test_upload_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock
        dic = Dictionary('123456')
        file_path = "test.tsv"
        name = "test name"

        with self.assertRaises(QTRestApiError):
            dic.upload(file_path, name)

    @patch("qt.dictionaries.requests.Session")
    def test_upload_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        dic = Dictionary('123456')
        file_path = "test.tsv"
        name = "test name"

        with self.assertRaises(QTConnectionError):
            dic.upload(file_path, name)
