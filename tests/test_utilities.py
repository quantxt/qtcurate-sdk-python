from unittest import TestCase, main
from unittest.mock import patch, Mock
from qtcurate.exceptions import *
from qtcurate.utilities import connect, json_to_tuple
import requests
from collections import namedtuple


class TestUtilities(TestCase):

    # Testing json_to_tuple function
    def test_json_to_tuple_arg_err(self):
        with self.assertRaises(QtArgumentError):
            json_to_tuple(())

    def test_json_to_tuple(self):
        some_dict = {'global': '123', 'key': 'value'}
        some_other_dict = {'key': 'value', 'Global': '123'}
        res_obj = namedtuple('Object', some_other_dict.keys())
        res = res_obj(**some_other_dict)

        self.assertEqual(res, json_to_tuple(some_dict))

    # Testing connect function
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

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_get_data_type_none_qt_rest_api_err(self, session):
        response = Mock()
        response.status_code = 401
        session.return_value.get.return_value = response

        with self.assertRaises(QtRestApiError):
            connect(method='get', uri='some_uri', headers='some_headers')

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_get_data_type_params_conn_err(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='get', uri='some_uri', headers='some_headers', data_type="params")

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_get_data_type_params_qt_rest_api_err(self, session):
        response = Mock()
        response.status_code = 401
        session.return_value.get.return_value = response

        with self.assertRaises(QtRestApiError):
            connect(method='get', uri='some_uri', headers='some_headers')

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_delete_conn_err(self, session):
        mock = Mock()
        mock.delete.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='delete', uri='some_uri', headers='some_headers')

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_delete_qt_rest_api_err(self, session):
        response = Mock()
        response.status_code = 401
        session.return_value.delete.return_value = response

        with self.assertRaises(QtRestApiError):
            connect(method='delete', uri='some_uri', headers='some_headers')

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_post_data_type_data_conn_err(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='post', uri='some_uri', headers='some_headers', data_type="data")

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_post_data_type_data_qt_rest_api_err(self, session):
        response = Mock()
        response.status_code = 401
        session.return_value.post.return_value = response

        with self.assertRaises(QtRestApiError):
            connect(method='post', uri='some_uri', headers='some_headers', data_type="data")

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_post_data_type_files_conn_err(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='post', uri='some_uri', headers='some_headers', data_type="files")

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_post_data_type_files_qt_rest_api_err(self, session):
        response = Mock()
        response.status_code = 401
        session.return_value.post.return_value = response

        with self.assertRaises(QtRestApiError):
            connect(method='post', uri='some_uri', headers='some_headers', data_type="files")

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_put_data_type_data_conn_err(self, session):
        mock = Mock()
        mock.put.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='put', uri='some_uri', headers='some_headers', data_type="data")

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_put_data_type_data_qt_rest_api_err(self, session):
        response = Mock()
        response.status_code = 401
        session.return_value.put.return_value = response

        with self.assertRaises(QtRestApiError):
            connect(method='put', uri='some_uri', headers='some_headers', data_type="data")

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_put_data_type_files_conn_err(self, session):
        mock = Mock()
        mock.put.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        with self.assertRaises(QtConnectionError):
            connect(method='put', uri='some_uri', headers='some_headers', data_type="files")

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_put_data_type_files_qt_rest_api_err(self, session):
        response = Mock()
        response.status_code = 401
        session.return_value.put.return_value = response

        with self.assertRaises(QtRestApiError):
            connect(method='put', uri='some_uri', headers='some_headers', data_type="files")

    def test_connect_method_put_arg_err(self):
        with self.assertRaises(QtArgumentError):
            connect(method='put', uri='some_uri', headers='some_headers', data_type="params")

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_equal_get(self, session):
        response = Mock()
        response.status_code = 200
        session.return_value.get.return_value = response

        result = connect(method='get', uri='some_uri', headers='some_headers')
        self.assertEqual(response, result)

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_get_data_type_params(self, session):
        response = Mock()
        response.status_code = 200
        session.return_value.get.return_value = response

        result = connect(method='get', uri='some_uri', headers='some_headers', data_type="params")
        self.assertEqual(response, result)

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_delete(self, session):
        response = Mock()
        response.status_code = 200
        session.return_value.delete.return_value = response

        result = connect(method='delete', uri='some_uri', headers='some_headers')
        self.assertEqual(response, result)

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_post_data_type_data(self, session):
        response = Mock()
        response.status_code = 200
        session.return_value.post.return_value = response

        result = connect(method='post', uri='some_uri', headers='some_headers', data_type="data")
        self.assertEqual(response, result)

    @patch("qtcurate.utilities.requests.Session")
    def test_connect_method_put_data_type_data(self, session):
        response = Mock()
        response.status_code = 200
        session.return_value.put.return_value = response

        result = connect(method='put', uri='some_uri', headers='some_headers', data_type="data")
        self.assertEqual(response, result)


if __name__ == '__main__':
    main()
