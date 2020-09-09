from unittest import TestCase
from qtcurate.dataprocess import DataProcess
from qtcurate.exceptions import *
from qtcurate.data_types import ChunkMode, SearchMode, DataType, HtmlParseMode, DictionaryType, AnalyzeMode


API_KEY = 'a5334f7d-2aac-44b3-aefc-a25cd9dd7bec'


class TestDataProcess(TestCase):

    def test_get_id(self):
        some_id = None
        tag = DataProcess(API_KEY)
        self.assertEqual(tag.get_id(), str(some_id))

    def test_set_id(self):
        tag = DataProcess(API_KEY)
        tag.set_id('some id')
        self.assertEqual(tag.get_id(), 'some id')
    # ??????
    def test_set_id_arg_not_str(self):
        tag = DataProcess(API_KEY)
        tag.set_id([123])
        self.assertEqual(tag.get_id(), str([123]))
    #  ??????
    def test_set_chunk(self):
        tag = DataProcess(API_KEY)
        chunk = ChunkMode.NONE
        tag.set_chunk(chunk)
        self.assertEqual(tag.temp_dict["chunk"], chunk.value)

    def test_get_uuid(self):
        tag = DataProcess(API_KEY)
        some_uuid = None
        self.assertEqual(tag.get_uuid(), str(some_uuid))

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

    def test_set_workers_arg_err(self):
        value = '123'
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.set_workers(value)

    def test_set_workers(self):
        value = 123
        tag = DataProcess(API_KEY)
        tag.set_workers(value)
        self.assertEqual(tag.temp_dict["numWorkers"], value)

    def test_files(self):
        list_files = ["file1", "file2"]
        tag = DataProcess(API_KEY)
        tag.with_documents(list_files)
        self.assertEqual(list_files, tag.temp_dict['files'])

    def test_files_arg_error(self):
        list_files = "string"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.with_documents(list_files)

    def test_sources(self):
        list_files = ["file1", "file2"]
        tag = DataProcess(API_KEY)
        tag.sources(list_files)
        self.assertEqual(list_files, tag.temp_dict['sources'])

    def test_sources_arg_error(self):
        list_files = "string"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.sources(list_files)

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
        tag.with_documents(["file1"])
        tag.urls(["123"])
        tag.search_rule(vocab_id)
        with self.assertRaises(QtDataProcessError):
            tag.create()

    def test_fetch_dp_id_arg_err(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.fetch(dp_id=[])

    def test_update_dp_id_arg_error(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.update(dp_id=[], update_files=["test.txt"])

    def test_update_list_arg_err(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.update(dp_id="some_id", update_files="file")

    def test_clone_dp_id_arg_err(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.clone(dp_id=[])

    def test_delete_argument_type_error(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.delete(dp_id=[])

    def test_progress_argument_type_error(self):
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.progress(dp_id=[])

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

    def test_report_to_xlsx_path_str_arg(self):
        path = 132
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.report_to_xlsx(path)

    def test_report_to_xlsx_path_permission(self):
        path = "/usr/bin/path.txt"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.report_to_xlsx(path)

    def test_report_to_xlsx_extension(self):
        path = "path.txt"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtFileTypeError):
            tag.report_to_xlsx(path)

    def test_report_to_json_path_str_arg(self):
        path = 132
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.report_to_json(path)

    def test_json_path_permission(self):
        path = "/usr/bin/path.txt"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtArgumentError):
            tag.report_to_json(path)

    def test_report_to_json_extension(self):
        path = "path.txt"
        tag = DataProcess(API_KEY)
        with self.assertRaises(QtFileTypeError):
            tag.report_to_json(path)
