from unittest import TestCase
import requests
from unittest.mock import patch, Mock

from qtcurate.dataprocess import DataProcess, DictionaryType
from qtcurate.exceptions import *


class TestDataProcess(TestCase):

    def test_title(self):
        title = "some title"
        tag = DataProcess('123456')
        tag.title(title)
        self.assertEqual(title, tag.temp_dict["title"])

    def test_title_arg_error(self):
        title = 12
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.title(title)

    def test_index(self):
        index = "some index"
        tag = DataProcess('123456')
        tag.index(index)
        self.assertEqual(index, tag.temp_dict["index"])

    def test_index_arg_error(self):
        index = [123]
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.index(index)

    def test_autotag(self):
        value = True
        tag = DataProcess('123456')
        tag.autotag(value)
        self.assertEqual(value, tag.temp_dict["get_phrases"])

    def test_autotag_arg_error(self):
        value = 12
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.autotag(value)

    def test_max_token(self):
        value = 1
        tag = DataProcess('123456')
        tag.max_token_per_utt(value)
        self.assertEqual(value, tag.temp_dict["maxTokenPerUtt"])

    def test_max_token_arg_error(self):
        value = "text"
        tag = DataProcess('123456')

        with self.assertRaises(QtArgumentError):
            tag.max_token_per_utt(value)

    def test_min_token(self):
        value = 1
        tag = DataProcess('123456')
        tag.min_token_per_utt(value)
        self.assertEqual(value, tag.temp_dict["minTokenPerUtt"])

    def test_min_token_arg_error(self):
        value = "text"
        tag = DataProcess('123456')

        with self.assertRaises(QtArgumentError):
            tag.min_token_per_utt(value)

    def test_exclude_utt(self):
        value = True
        tag = DataProcess('123456')
        tag.exclude_utt_without_entities(value)
        self.assertEqual(value, tag.temp_dict["exclude_utt_without_entities"])

    def test_exclude_utt_arg_error(self):
        value = 12
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.exclude_utt_without_entities(value)

    def test_regex_pattern(self):
        value = 12
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.regex_pattern(value)

    def test_regex_group(self):
        value = 12
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.regex_group(value)

    def test_files(self):
        list_files = ["file1", "file2"]
        tag = DataProcess('123456')
        tag.files(list_files)
        self.assertEqual(list_files, tag.temp_dict['files'])

    def test_files_arg_error(self):
        list_files = "string"
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.files(list_files)

    def test_urls(self):
        list_urls = ["www.url1.com", "www.url2.com"]
        tag = DataProcess('123456')
        tag.urls(list_urls)
        self.assertEqual(list_urls, tag.temp_dict['urls'])

    def test_urls_arg_error(self):
        list_urls = "string"
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.urls(list_urls)

    def test_search_rule(self):
        dic = dict()
        path = "file path"
        vocab = DictionaryType.NONE
        dic["vocabPath"] = path
        dic["vocabValueType"] = vocab.value
        search_dict = [dic]
        tag = DataProcess('123456')
        tag.search_rule(path, vocab)
        self.assertEqual(search_dict, tag.temp_dict['searchDictionaries'])

    def test_search_path_arg_error(self):
        dic = dict()
        path = 1234
        vocab = DictionaryType.NONE
        dic["vocabPath"] = path
        dic["vocabValueType"] = vocab.value
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.search_rule(path, vocab)

    def test_search_vocab_arg_error(self):
        dic = dict()
        path = "path"
        vocab = 1
        dic["vocabPath"] = path
        dic["vocabValueType"] = vocab
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.search_rule(path, vocab)

    def test_upload_arg_error(self):
        file = 123
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.upload(file)

    def test_upload_file_type(self):
        file = "path"
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.upload(file)

    def test_upload_file_exists(self):
        file = "path.txt"
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.upload(file)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_upload_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock
        tag = DataProcess('123456')
        file_path = "test.txt"

        with self.assertRaises(QtRestApiError):
            tag.upload(file_path)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_upload_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess('123456')
        file_path = "test.txt"

        with self.assertRaises(QtConnectionError):
            tag.upload(file_path)

    def test_dataprocess_empty_files(self):
        dic = dict()
        path = "file path"
        vocab = DictionaryType.NONE
        dic["vocabPath"] = path
        dic["vocabValueType"] = vocab.value
        tag = DataProcess('123456')
        tag.search_rule(path, vocab)
        self.assertRaises(QtDataProcessError, tag.tagging_files)

    def test_dataprocess_empty_dictionary(self):
        path = ["file path"]
        tag = DataProcess('123456')
        tag.files(path)
        self.assertRaises(QtDataProcessError, tag.tagging_files)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_dataprocess_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock

        list_files = ['test.txt']
        dict_path = "test.txt"
        vocal_value_type = DictionaryType.NONE
        tag = DataProcess('123456')
        tag.files(list_files)
        tag.search_rule(dict_path, vocal_value_type)

        self.assertRaises(QtRestApiError, tag.tagging_files)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_dataprocess_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        list_files = ['test.txt']
        dict_path = "test.txt"
        vocal_value_type = DictionaryType.NONE
        tag = DataProcess('123456')
        tag.files(list_files)
        tag.search_rule(dict_path, vocal_value_type)

        self.assertRaises(QtConnectionError, tag.tagging_files)

    def test_delete_arg_error(self):
        value = 12
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.delete(value)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_delete_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.delete.return_value = response
        session.return_value = mock
        tag = DataProcess('123456')
        tag_id = "some tag id"

        with self.assertRaises(QtRestApiError):
            tag.delete(tag_id)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_delete_connection_exception(self, session):
        mock = Mock()
        mock.delete.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess('123456')
        tag_id = "some tag id"

        with self.assertRaises(QtConnectionError):
            tag.delete(tag_id)

    def test_mininig_empty_urls(self):
        dic = dict()
        path = "file path"
        vocab = DictionaryType.NONE
        dic["vocabPath"] = path
        dic["vocabValueType"] = vocab.value
        tag = DataProcess('123456')
        tag.search_rule(path, vocab)
        self.assertRaises(QtDataProcessError, tag.mining_url)

    def test_dataprocess_empty_dictionary(self):
        urls = ["www.url.com"]
        tag = DataProcess('123456')
        tag.urls(urls)
        self.assertRaises(QtDataProcessError, tag.mining_url)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_mining_url_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock

        list_urls = ['test.txt']
        dict_path = "test.txt"
        vocal_value_type = DictionaryType.NONE
        tag = DataProcess('123456')
        tag.urls(list_urls)
        tag.search_rule(dict_path, vocal_value_type)

        self.assertRaises(QtRestApiError, tag.mining_url)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_mining_url_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        list_urls = ['test.txt']
        dict_path = "test.txt"
        vocal_value_type = DictionaryType.NONE
        tag = DataProcess('123456')
        tag.urls(list_urls)
        tag.search_rule(dict_path, vocal_value_type)

        self.assertRaises(QtConnectionError, tag.mining_url)

    def test_progress_arg_error(self):
        index = 123
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.progress(index)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_progress_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        tag = DataProcess('123456')

        self.assertRaises(QtRestApiError, tag.progress)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_progress_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess('123456')

        self.assertRaises(QtConnectionError, tag.progress)

    def test_search_index_arg(self):
        index = 123
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.search(index)

    def test_search_param_from_arg(self):
        index = "test"
        param_from = "test"
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.search(index, param_from)

    def test_search_size_range_arg(self):
        index = "test"
        param_from = 5
        size = 201
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.search(index, param_from, size)

    def test_search_size_not_int_arg(self):
        index = "test"
        param_from = 5
        size = "test"
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.search(index, param_from, size)

    def test_search_pairs_arg(self):
        index = "test"
        param_from = 5
        size = 100
        tag = DataProcess('123456')
        f1 = "string"
        with self.assertRaises(QtArgumentError):
            tag.search(index, param_from, size, f1)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_search_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        tag = DataProcess('123456')
        string = "some string"

        with self.assertRaises(QtRestApiError):
            tag.search(string)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_search_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess('123456')
        string = "some string"

        with self.assertRaises(QtConnectionError):
            tag.search(string)

    def test_xlsx_index_arg(self):
        index = 123
        path = "path"
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.report_to_xlsx(index, path)

    def test_xlsx_path_str_arg(self):
        index = "index"
        path = 132
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.report_to_xlsx(index, path)

    def test_xlsx_path_permission(self):
        index = "index"
        path = "/usr/bin/path.txt"
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.report_to_xlsx(index, path)

    def test_xlsx_extension(self):
        index = "index"
        path = "path.txt"
        tag = DataProcess('123456')
        with self.assertRaises(QtFileTypeError):
            tag.report_to_xlsx(index, path)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_xlsx_report_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        tag = DataProcess('123456')
        element = "some string"
        path = "test.xlsx"

        with self.assertRaises(QtRestApiError):
            tag.report_to_xlsx(element, path)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_xlsx_report_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess('123456')
        element = "some string"
        path = "test.xlsx"

        with self.assertRaises(QtConnectionError):
            tag.report_to_xlsx(element, path)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_json_report_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        tag = DataProcess('123456')
        element = "some string"
        path = "test.json"

        with self.assertRaises(QtRestApiError):
            tag.report_to_json(element, path)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_json_report_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess('123456')
        element = "some string"
        path = "test.json"

        with self.assertRaises(QtConnectionError):
            tag.report_to_json(element, path)

    def test_json_index_arg(self):
        index = 123
        path = "path"
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.report_to_json(index, path)

    def test_json_path_str_arg(self):
        index = "index"
        path = 132
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.report_to_json(index, path)

    def test_json_path_permission(self):
        index = "index"
        path = "/usr/bin/path.txt"
        tag = DataProcess('123456')
        with self.assertRaises(QtArgumentError):
            tag.report_to_json(index, path)

    def test_json_extension(self):
        index = "index"
        path = "path.txt"
        tag = DataProcess('123456')
        with self.assertRaises(QtFileTypeError):
            tag.report_to_json(index, path)
