from unittest import TestCase
import requests
from unittest.mock import patch, Mock

from qtcurate.tagging import Tagging, DictionaryType
from qtcurate.exceptions import *


class TestTagging(TestCase):

    def test_title(self):
        title = "some title"
        tag = Tagging('123456')
        tag.title(title)
        self.assertEqual(title, tag.temp_dict["title"])

    def test_title_arg_error(self):
        title = 12
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.title(title)

    def test_index(self):
        index = "some index"
        tag = Tagging('123456')
        tag.index(index)
        self.assertEqual(index, tag.temp_dict["index"])

    def test_index_arg_error(self):
        index = [123]
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.index(index)

    def test_autotag(self):
        value = True
        tag = Tagging('123456')
        tag.autotag(value)
        self.assertEqual(value, tag.temp_dict["autotag"])

    def test_autotag_arg_error(self):
        value = 12
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.autotag(value)

    def test_max_token(self):
        value = 1
        tag = Tagging('123456')
        tag.max_token_per_utt(value)
        self.assertEqual(value, tag.temp_dict["maxTokenPerUtt"])

    def test_max_token_arg_error(self):
        value = "text"
        tag = Tagging('123456')

        with self.assertRaises(QTArgumentError):
            tag.max_token_per_utt(value)

    def test_min_token(self):
        value = 1
        tag = Tagging('123456')
        tag.min_token_per_utt(value)
        self.assertEqual(value, tag.temp_dict["minTokenPerUtt"])

    def test_min_token_arg_error(self):
        value = "text"
        tag = Tagging('123456')

        with self.assertRaises(QTArgumentError):
            tag.min_token_per_utt(value)

    def test_exclude_utt(self):
        value = True
        tag = Tagging('123456')
        tag.exclude_utt_without_entities(value)
        self.assertEqual(value, tag.temp_dict["exclude_utt_without_entities"])

    def test_exclude_utt_arg_error(self):
        value = 12
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.exclude_utt_without_entities(value)

    def test_files(self):
        list_files = ["file1", "file2"]
        tag = Tagging('123456')
        tag.files(list_files)
        self.assertEqual(list_files, tag.temp_dict['files'])

    def test_files_arg_error(self):
        list_files = "string"
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.files(list_files)

    def test_urls(self):
        list_urls = ["www.url1.com", "www.url2.com"]
        tag = Tagging('123456')
        tag.urls(list_urls)
        self.assertEqual(list_urls, tag.temp_dict['urls'])

    def test_urls_arg_error(self):
        list_urls = "string"
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.urls(list_urls)

    def test_search_rule(self):
        dic = dict()
        path = "file path"
        vocab = DictionaryType.NONE
        dic["vocabPath"] = path
        dic["vocabValueType"] = vocab.value
        search_dict = [dic]
        tag = Tagging('123456')
        tag.search_rule(path, vocab)
        self.assertEqual(search_dict, tag.temp_dict['searchDictionaries'])

    def test_search_path_arg_error(self):
        dic = dict()
        path = 1234
        vocab = DictionaryType.NONE
        dic["vocabPath"] = path
        dic["vocabValueType"] = vocab.value
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.search_rule(path, vocab)

    def test_search_vocab_arg_error(self):
        dic = dict()
        path = "path"
        vocab = 1
        dic["vocabPath"] = path
        dic["vocabValueType"] = vocab
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.search_rule(path, vocab)

    def test_upload_arg_error(self):
        file = 123
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.upload(file)

    def test_upload_file_type(self):
        file = "path"
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.upload(file)

    def test_upload_file_exists(self):
        file = "path.txt"
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.upload(file)

    @patch("qtcurate.tagging.requests.Session")
    def test_upload_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock
        tag = Tagging('123456')
        file_path = "test.txt"

        with self.assertRaises(QTRestApiError):
            tag.upload(file_path)

    @patch("qtcurate.tagging.requests.Session")
    def test_upload_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = Tagging('123456')
        file_path = "test.txt"

        with self.assertRaises(QTConnectionError):
            tag.upload(file_path)

    def test_tagging_empty_files(self):
        dic = dict()
        path = "file path"
        vocab = DictionaryType.NONE
        dic["vocabPath"] = path
        dic["vocabValueType"] = vocab.value
        tag = Tagging('123456')
        tag.search_rule(path, vocab)
        self.assertRaises(QTTaggingError, tag.tagging_files)

    def test_tagging_empty_dictionary(self):
        path = ["file path"]
        tag = Tagging('123456')
        tag.files(path)
        self.assertRaises(QTTaggingError, tag.tagging_files)

    @patch("qtcurate.tagging.requests.Session")
    def test_tagging_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock

        list_files = ['test.txt']
        dict_path = "test.txt"
        vocal_value_type = DictionaryType.NONE
        tag = Tagging('123456')
        tag.files(list_files)
        tag.search_rule(dict_path, vocal_value_type)

        self.assertRaises(QTRestApiError, tag.tagging_files)

    @patch("qtcurate.tagging.requests.Session")
    def test_tagging_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        list_files = ['test.txt']
        dict_path = "test.txt"
        vocal_value_type = DictionaryType.NONE
        tag = Tagging('123456')
        tag.files(list_files)
        tag.search_rule(dict_path, vocal_value_type)

        self.assertRaises(QTConnectionError, tag.tagging_files)

    def test_delete_arg_error(self):
        value = 12
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.delete(value)

    @patch("qtcurate.tagging.requests.Session")
    def test_delete_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.delete.return_value = response
        session.return_value = mock
        tag = Tagging('123456')
        tag_id = "some tag id"

        with self.assertRaises(QTRestApiError):
            tag.delete(tag_id)

    @patch("qtcurate.tagging.requests.Session")
    def test_delete_connection_exception(self, session):
        mock = Mock()
        mock.delete.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = Tagging('123456')
        tag_id = "some tag id"

        with self.assertRaises(QTConnectionError):
            tag.delete(tag_id)

    def test_mininig_empty_urls(self):
        dic = dict()
        path = "file path"
        vocab = DictionaryType.NONE
        dic["vocabPath"] = path
        dic["vocabValueType"] = vocab.value
        tag = Tagging('123456')
        tag.search_rule(path, vocab)
        self.assertRaises(QTTaggingError, tag.mining_url)

    def test_tagging_empty_dictionary(self):
        urls = ["www.url.com"]
        tag = Tagging('123456')
        tag.urls(urls)
        self.assertRaises(QTTaggingError, tag.mining_url)

    @patch("qtcurate.tagging.requests.Session")
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
        tag = Tagging('123456')
        tag.urls(list_urls)
        tag.search_rule(dict_path, vocal_value_type)

        self.assertRaises(QTRestApiError, tag.mining_url)

    @patch("qtcurate.tagging.requests.Session")
    def test_mining_url_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        list_urls = ['test.txt']
        dict_path = "test.txt"
        vocal_value_type = DictionaryType.NONE
        tag = Tagging('123456')
        tag.urls(list_urls)
        tag.search_rule(dict_path, vocal_value_type)

        self.assertRaises(QTConnectionError, tag.mining_url)

    def test_progress_arg_error(self):
        index = 123
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.progress(index)

    @patch("qtcurate.tagging.requests.Session")
    def test_progress_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        tag = Tagging('123456')

        self.assertRaises(QTRestApiError, tag.progress)

    @patch("qtcurate.tagging.requests.Session")
    def test_progress_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = Tagging('123456')

        self.assertRaises(QTConnectionError, tag.progress)

    def test_search_index_arg(self):
        index = 123
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.search(index)

    def test_search_param_from_arg(self):
        index = "test"
        param_from = "test"
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.search(index, param_from)

    def test_search_size_range_arg(self):
        index = "test"
        param_from = 5
        size = 201
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.search(index, param_from, size)

    def test_search_size_not_int_arg(self):
        index = "test"
        param_from = 5
        size = "test"
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.search(index, param_from, size)

    def test_search_pairs_arg(self):
        index = "test"
        param_from = 5
        size = 100
        tag = Tagging('123456')
        f1 = "string"
        with self.assertRaises(QTArgumentError):
            tag.search(index, param_from, size, f1)

    @patch("qtcurate.tagging.requests.Session")
    def test_search_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        tag = Tagging('123456')
        string = "some string"

        with self.assertRaises(QTRestApiError):
            tag.search(string)

    @patch("qtcurate.tagging.requests.Session")
    def test_search_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = Tagging('123456')
        string = "some string"

        with self.assertRaises(QTConnectionError):
            tag.search(string)

    def test_xlsx_index_arg(self):
        index = 123
        path = "path"
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.report_to_xlsx(index, path)

    def test_xlsx_path_str_arg(self):
        index = "index"
        path = 132
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.report_to_xlsx(index, path)

    def test_xlsx_path_permission(self):
        index = "index"
        path = "/usr/bin/path.txt"
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.report_to_xlsx(index, path)

    def test_xlsx_extension(self):
        index = "index"
        path = "path.txt"
        tag = Tagging('123456')
        with self.assertRaises(QTFileTypeError):
            tag.report_to_xlsx(index, path)

    @patch("qtcurate.tagging.requests.Session")
    def test_xlsx_report_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        tag = Tagging('123456')
        element = "some string"
        path = "test.xlsx"

        with self.assertRaises(QTRestApiError):
            tag.report_to_xlsx(element, path)

    @patch("qtcurate.tagging.requests.Session")
    def test_xlsx_report_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = Tagging('123456')
        element = "some string"
        path = "test.xlsx"

        with self.assertRaises(QTConnectionError):
            tag.report_to_xlsx(element, path)

    @patch("qtcurate.tagging.requests.Session")
    def test_json_report_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        tag = Tagging('123456')
        element = "some string"
        path = "test.json"

        with self.assertRaises(QTRestApiError):
            tag.report_to_json(element, path)

    @patch("qtcurate.tagging.requests.Session")
    def test_json_report_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = Tagging('123456')
        element = "some string"
        path = "test.json"

        with self.assertRaises(QTConnectionError):
            tag.report_to_json(element, path)

    def test_json_index_arg(self):
        index = 123
        path = "path"
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.report_to_json(index, path)

    def test_json_path_str_arg(self):
        index = "index"
        path = 132
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.report_to_json(index, path)

    def test_json_path_permission(self):
        index = "index"
        path = "/usr/bin/path.txt"
        tag = Tagging('123456')
        with self.assertRaises(QTArgumentError):
            tag.report_to_json(index, path)

    def test_json_extension(self):
        index = "index"
        path = "path.txt"
        tag = Tagging('123456')
        with self.assertRaises(QTFileTypeError):
            tag.report_to_json(index, path)
