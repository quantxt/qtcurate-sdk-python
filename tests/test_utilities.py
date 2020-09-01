from unittest import TestCase
from unittest.mock import patch, Mock
from qtcurate.exceptions import QtConnectionError, QtArgumentError
from qtcurate.utilities import connect, json_to_tuple
import requests


class TestUtilities(TestCase):

    def test_json_to_tuple_arg_err(self):
        with self.assertRaises(QtArgumentError):
            json_to_tuple(())

    def test_connect_data_type_arg_err(self):
        with self.assertRaises(QtArgumentError):
            connect(method='some_method', uri='some_uri', headers='some_headers', data_type='123')

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_get_data_type_none_conn_err(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='get', uri='some_uri', headers='some_headers')

    @patch("qtcurate.qtdict.requests.Session")
    def test_connect_method_get_data_type_params_conn_err(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='get', uri='some_uri', headers='some_headers', data_type='params')

    @patch("qtcurate.qtdict.requests.Session")
    def test_connect_method_delete_conn_err(self, session):
        mock = Mock()
        mock.delete.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='delete', uri='some_uri', headers='some_headers', data_type=None)

    @patch("qtcurate.qtdict.requests.Session")
    def test_connect_method_post_data_type_data_conn_err(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='post', uri='some_uri', headers='some_headers', data_type='data')

    @patch("qtcurate.qtdict.requests.Session")
    def test_connect_method_post_data_type_files_conn_err(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='post', uri='some_uri', headers='some_headers', data_type='files')

    @patch("qtcurate.qtdict.requests.Session")
    def test_connect_method_put_data_type_data_conn_err(self, session):
        mock = Mock()
        mock.put.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='put', uri='some_uri', headers='some_headers', data_type='data')

    @patch("qtcurate.qtdict.requests.Session")
    def test_connect_method_put_data_type_files_conn_err(self, session):
        mock = Mock()
        mock.put.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='put', uri='some_uri', headers='some_headers', data_type='files')
