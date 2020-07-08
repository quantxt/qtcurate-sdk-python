from unittest import TestCase
import requests
from unittest.mock import patch, Mock

from qtcurate.dataprocess import DataProcess
from qtcurate.exceptions import *
from qtcurate.data_types import ChunkMode, SearchMode, DataType, HtmlParseMode, DictionaryType, AnalyzeMode


API_KEY = 'some_key'


class TestDataProcess(TestCase):

    def test_title(self):
        title = "some title"
        tag = DataProcess(API_KEY)
        tag.title(title)
        self.assertEqual(title, tag.temp_dict["title"])

    def test_title_arg_error(self):
        title = 12
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.title(title)

    def test_query(self):
        query = "some query"
        tag = DataProcess(API_KEY)
        tag.query(query)
        self.assertEqual(query, tag.temp_dict["query"])

    def test_query_arg_error(self):
        query = 12
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.query(query)

    def test_stitle(self):
        stitle = "some stitle"
        tag = DataProcess(API_KEY)
        tag.stitle(stitle)
        self.assertEqual(stitle, tag.temp_dict["stitle"])

    def test_stitle_arg_error(self):
        stitle = 12
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.query(stitle)

    def test_sort_by_position(self):
        value = True
        tag = DataProcess(API_KEY)
        tag.sort_by_position(value)
        self.assertEqual(value, tag.temp_dict["sortByPosition"])

    def test_sort_by_position_arg_error(self):
        value = 12
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.sort_by_position(value)

    def test_exclude_utt(self):
        value = True
        tag = DataProcess(API_KEY)
        tag.exclude_utt_without_entities(value)
        self.assertEqual(value, tag.temp_dict["excludeUttWithoutEntities"])

    def test_exclude_utt_arg_error(self):
        value = 12
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.exclude_utt_without_entities(value)

    def test_files(self):
        list_files = ["file1", "file2"]
        tag = DataProcess(API_KEY)
        tag.files(list_files)
        self.assertEqual(list_files, tag.temp_dict['files'])

    def test_files_arg_error(self):
        list_files = "string"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.files(list_files)

    def test_urls(self):
        list_urls = ["www.url1.com", "www.url2.com"]
        tag = DataProcess(API_KEY)
        tag.urls(list_urls)
        self.assertEqual(list_urls, tag.temp_dict['urls'])

    def test_urls_arg_error(self):
        list_urls = "string"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.urls(list_urls)

    def test_search_rule(self):
        dic = dict()
        vocab_id = "some id"
        dic["vocabId"] = vocab_id
        search_dict = [dic]
        tag = DataProcess(API_KEY)
        tag.search_rule(vocab_id)
        self.assertEqual(search_dict, tag.temp_dict['searchDictionaries'])

    def test_search_rule_vocab_id_input_error(self):
        vocab_id = 1234
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id)

    def test_search_rule_vocab_value_type_error(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id, vocab_value_type_input=123)

    def test_search_rule_vocab_value_regex(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id, vocab_value_type_input=DictionaryType.REGEX)

    def test_search_rule_vocab_value_phrase_matching_pattern_invalid_str(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id, vocab_value_type_input=DictionaryType.REGEX, re_phrase_matching_pattern="[")

    def test_search_rule_vocab_value_phrase_matching_pattern_invalid_type(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id, vocab_value_type_input=DictionaryType.REGEX, re_phrase_matching_pattern=123)

    def test_search_rule_skip_pattern_between_key_and_value_invalid_type(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id, skip_pattern_between_key_and_value=[])

    def test_search_rule_skip_pattern_between_values_invalid_type(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id, skip_pattern_between_values=[])

    def test_search_rule_stopword_list_invalid_type(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id, stopword_list=[])

    def test_search_rule_synonim_list_invalid_type(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id, synonim_list=[])

    def test_search_rule_search_mode_invalid_type(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id, search_mode=[])

    def test_search_rule_analyze_mode_invalid_type(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search_rule(vocab_id, analyze_mode=[])

    def test_upload_arg_error(self):
        file = 123
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.upload(file)

    def test_upload_file_type(self):
        file = "path"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.upload(file)

    def test_upload_file_exists(self):
        file = "path.txt"
        tag = DataProcess(API_KEY)
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
        tag = DataProcess(API_KEY)
        file_path = "test.txt"

        with self.assertRaises(QtRestApiError):
            tag.upload(file_path)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_upload_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess(API_KEY)
        file_path = "test.txt"

        with self.assertRaises(QtConnectionError):
            tag.upload(file_path)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_upload(self, session):
        dic = {'uuid': '2d3e39e4-fe7d-493b-b4f0-b275a1147ffe',
               'username': 'mbjelanovic@gmail.com',
               'fileName': 'links.txt',
               'link': 'http://portal.files.quantxt.com/mbjelanovic@gmail.com/2d3e39e4-fe7d-493b-b4f0-b275a1147ffe',
               'date': '2020-07-05T17:13:44.579029',
               'contentType': 'text/plain',
               'source': 'links.txt'}
        mock = Mock()
        response = Mock()
        response.status_code = 200
        response.json.return_value = dic
        mock.post.return_value = response
        session.return_value = mock

        tag = DataProcess(API_KEY)
        file = "test.txt"
        self.assertEqual(tag.upload(file), dic)

    def test_create_empty_search_dict(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtDataProcessError):
            tag.create()

    def test_crete_query_is_requested(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        tag.temp_dict["query"] = {}
        tag.sources(["file1", "file2"])
        tag.search_rule(vocab_id)
        with self.assertRaises(QtDataProcessError):
            tag.create()

    def test_crete_choose_one_kind(self):
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        tag.files(["file1"])
        tag.urls(["123"])
        tag.search_rule(vocab_id)
        with self.assertRaises(QtDataProcessError):
            tag.create()

    @patch("qtcurate.dataprocess.requests.Session")
    def test_create_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock

        list_files = ['test.txt']
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        tag.files(list_files)
        tag.search_rule(vocab_id)
        with self.assertRaises(QtRestApiError):
            tag.create()

    @patch("qtcurate.dataprocess.requests.Session")
    def test_create_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        list_files = ['test.txt']
        vocab_id = "some_id"
        tag = DataProcess(API_KEY)
        tag.files(list_files)
        tag.search_rule(vocab_id)
        with self.assertRaises(QtConnectionError):
            tag.create()

    @patch("qtcurate.dataprocess.requests.Session")
    def test_create(self, session):
        dic = {'id': 'pzenqasrtm',
               'title': None,
               'get_phrases': None,
               'maxTokenPerUtt': 35,
               'minTokenPerUtt': 6,
               'excludeUttWithoutEntities': True,
               'searchDictionaries': [{'vocabId': 'some_id',
                                       'vocabName': None,
                                       'vocabValueType': None,
                                       'language': 'ENGLISH',
                                       'stopwordList': None,
                                       'synonymList': None,
                                       'searchMode': 'SPAN',
                                       'analyzeStrategy': 'STEM',
                                       'skipPatternBetweenKeyAndValue': None,
                                       'skipPatternBetweenValues': None,
                                       'phraseMatchingPattern': None,
                                       'phraseMatchingGroups': None}
                                      ],
               'files': None,
               'insights': {'number_documents_in': None,
                            'number_documents_out': None,
                            'number_of_results': None,
                            'number_segments': None,
                            'number_bytes_in': None,
                            'took': None,
                            'start_time': 1594213819088,
                            'qtcurate_start': None,
                            'qtcurate_process_start': None,
                            'qtcurate_end': None
                            },
               'index': 'pzenqasrtm', 'stitle': None
               }
        mock = Mock()
        response = Mock()
        response.status_code = 200
        response.json.return_value = dic
        mock.post.return_value = response
        session.return_value = mock

        tag = DataProcess(API_KEY)
        vocab_id = "some_id"
        urls = ["www.url.com"]
        tag.urls(urls)
        tag.search_rule(vocab_id)
        self.assertEqual(tag.create(), dic)

    def test_update_dp_id_arg_error(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.update(dp_id=[], update_files=["test.txt"])

    def test_update_list_arg_err(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.clone(dp_id="some_id", update_files="file")

    @patch("qtcurate.dataprocess.requests.Session")
    def test_update_connection_exception(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess(API_KEY)
        with self.assertRaises(QtConnectionError):
            tag.update(dp_id="some_id", update_files=['test.txt'])

    @patch("qtcurate.dataprocess.requests.Session")
    def test_update_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock

        tag = DataProcess(API_KEY)
        with self.assertRaises(QtRestApiError):
            tag.clone(dp_id="some_id", update_files=[])

    def test_clone_dp_id_arg_err(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.clone(dp_id=[], update_files=["file"])

    def test_clone_update_list_arg_err(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.clone(dp_id="some_id", update_files="file")

    @patch("qtcurate.dataprocess.requests.Session")
    def test_clone_conn_error(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess(API_KEY)
        with self.assertRaises(QtConnectionError):
            tag.clone(dp_id="some_id", update_files=[])

    @patch("qtcurate.dataprocess.requests.Session")
    def test_clone_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock

        tag = DataProcess(API_KEY)
        with self.assertRaises(QtRestApiError):
            tag.clone(dp_id="some_id", update_files=[])

    def test_fetch_dp_id_arg_err(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.fetch(dp_id=[])

    @patch("qtcurate.dataprocess.requests.Session")
    def test_fetch_conn_error(self, session):
        mock = Mock()
        mock.post.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess(API_KEY)
        with self.assertRaises(QtConnectionError):
            tag.fetch(dp_id="some_id")

    @patch("qtcurate.dataprocess.requests.Session")
    def test_fetch_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.post.return_value = response
        session.return_value = mock

        tag = DataProcess(API_KEY)
        with self.assertRaises(QtRestApiError):
            tag.fetch(dp_id="some_id")

    def test_delete_argument_type_error(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.delete(dp_id=[])

    @patch("qtcurate.dataprocess.requests.Session")
    def test_delete_connection_exception(self, session):
        mock = Mock()
        mock.delete.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess(API_KEY)
        with self.assertRaises(QtConnectionError):
            tag.delete(dp_id="some_index")

    @patch("qtcurate.dataprocess.requests.Session")
    def test_delete_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.delete.return_value = response
        session.return_value = mock

        tag = DataProcess(API_KEY)
        with self.assertRaises(QtRestApiError):
            tag.delete(dp_id="some_index")

    def test_progress_argument_type_error(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.progress(dp_id=[])

    @patch("qtcurate.dataprocess.requests.Session")
    def test_progress_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess(API_KEY)
        with self.assertRaises(QtConnectionError):
            tag.progress(dp_id="some_index")

    @patch("qtcurate.dataprocess.requests.Session")
    def test_progress_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        tag = DataProcess(API_KEY)
        with self.assertRaises(QtRestApiError):
            tag.progress(dp_id="some_index")

    def test_search_dp_id_arg(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search(dp_id=123)

    def test_search_param_from_arg_error(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search(dp_id="some_dp", param_from="123")

    def test_search_size_range_arg(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search(dp_id="some_dp", param_from=5, size=201)

    def test_search_size_not_int_arg(self):
        dp_id = "test"
        param_from = 5
        size = "test"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.search(dp_id, param_from, size)

    def test_search_pairs_arg(self):
        index = "test"
        param_from = 5
        size = 100
        tag = DataProcess(API_KEY)
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

        tag = DataProcess(API_KEY)
        string = "some string"

        with self.assertRaises(QtRestApiError):
            tag.search(string)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_search_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess(API_KEY)
        string = "some string"
        with self.assertRaises(QtConnectionError):
            tag.search(string)

    def test_xlsx_index_arg(self):
        dp_id = 123
        path = "path"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.report_to_xlsx(dp_id, path)

    def test_xlsx_path_str_arg(self):
        dp_id = "some_id"
        path = 132
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.report_to_xlsx(dp_id, path)

    def test_xlsx_path_permission(self):
        dp_id = "some_id"
        path = "/usr/bin/path.txt"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.report_to_xlsx(dp_id, path)

    def test_xlsx_extension(self):
        dp_id = "some_id"
        path = "path.txt"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtFileTypeError):
            tag.report_to_xlsx(dp_id, path)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_xlsx_report_not_authorized(self, session):
        mock = Mock()
        response = Mock()
        response.status_code = 401
        response.json.return_value = []
        mock.get.return_value = response
        session.return_value = mock

        tag = DataProcess(API_KEY)
        element = "some string"
        path = "test.xlsx"

        with self.assertRaises(QtRestApiError):
            tag.report_to_xlsx(element, path)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_xlsx_report_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess(API_KEY)
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

        tag = DataProcess(API_KEY)
        element = "some string"
        path = "test.json"
        with self.assertRaises(QtRestApiError):
            tag.report_to_json(element, path)

    @patch("qtcurate.dataprocess.requests.Session")
    def test_json_report_connection_exception(self, session):
        mock = Mock()
        mock.get.side_effect = requests.exceptions.ConnectionError("Connection error")
        session.return_value = mock

        tag = DataProcess(API_KEY)
        element = "some string"
        path = "test.json"
        with self.assertRaises(QtConnectionError):
            tag.report_to_json(element, path)

    def test_json_index_arg(self):
        dp_id = 123
        path = "path"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.report_to_json(dp_id, path)

    def test_json_path_str_arg(self):
        dp_id = "some_id"
        path = 132
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.report_to_json(dp_id, path)

    def test_json_path_permission(self):
        dp_id = "some_id"
        path = "/usr/bin/path.txt"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.report_to_json(dp_id, path)

    def test_json_extension(self):
        dp_id = "some_id"
        path = "path.txt"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtFileTypeError):
            tag.report_to_json(dp_id, path)
