from unittest import TestCase, main
from qtcurate.dataprocess import DataProcess
from qtcurate.exceptions import *
from qtcurate.extractor import ChunkMode, Extractor, Type, Mode
from unittest.mock import patch, Mock
from qtcurate.vocabulary import json_to_tuple, connect


class TestDataProcess(TestCase):

    def test_get_id(self):
        some_id = None
        dataprocess = DataProcess()
        self.assertEqual(dataprocess.get_id(), str(some_id))

    def test_set_id(self):
        dataprocess = DataProcess()
        dataprocess.set_id('some id')
        self.assertEqual(dataprocess.id, 'some id')

    def test_set_chunk(self):
        dataprocess = DataProcess()
        some_chunk = ChunkMode.SENTENCE
        dataprocess.set_chunk(some_chunk)
        self.assertEqual(dataprocess.temp_dict["chunk"], some_chunk.value)

    def test_get_uuid(self):
        dataprocess = DataProcess()
        some_uuid = None
        self.assertEqual(dataprocess.get_uuid(), str(some_uuid))

    def test_set_description(self):
        title = "some title"
        dataprocess = DataProcess()
        dataprocess.set_description(title)
        self.assertEqual(title, dataprocess.temp_dict["title"])

    def test_set_description_arg_error(self):
        title = 12
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.set_description(title)

    def test_exclude_utt(self):
        value = True
        dataprocess = DataProcess()
        dataprocess.exclude_utt_without_entities(value)
        self.assertEqual(value, dataprocess.temp_dict["excludeUttWithoutEntities"])

    def test_exclude_utt_arg_error(self):
        value = 12
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.exclude_utt_without_entities(value)

    def test_set_workers_arg_err(self):
        value = '123'
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.set_workers(value)

    def test_set_workers(self):
        value = 123
        dataprocess = DataProcess()
        dataprocess.set_workers(value)
        self.assertEqual(dataprocess.temp_dict["numWorkers"], value)

    def test_with_documents(self):
        list_files = ["file1", "file2"]
        dataprocess = DataProcess()
        dataprocess.with_documents(list_files)
        self.assertEqual(list_files, dataprocess.temp_dict['files'])

    def test_with_documents_arg_error(self):
        list_files = "string"
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.with_documents(list_files)

    def test_add_extractor(self):
        ex = Extractor()
        ex.set_vocabulary('123')
        ex.set_type(Type.DATETIME)
        ex.set_mode(Mode.SIMPLE)
        ex.set_stop_word_list(['stop'])
        ex.set_synonym_list(['synonym'])
        ex.set_validator('val')
        some_list = [{'vocabId': '123',
                      'vocabValueType': 'REGEX',
                      'dataType': 'DATETIME',
                      'searchMode': 'ORDERED_SPAN',
                      'analyzeStrategy': 'SIMPLE',
                      'stopwordList': ['stop'],
                      'synonymList': ['synonym'],
                      'phraseMatchingPattern': 'val'}]

        dataprocess = DataProcess()
        dataprocess.add_extractor(ex)
        self.assertEqual(dataprocess.temp_dict["searchDictionaries"], some_list)

    def test_add_extractor_regex_err(self):
        ex = Extractor()
        ex.set_validator('[')
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.add_extractor(ex)

    def test_get_extractor(self):
        some_dict = {'searchDictionaries': 'ab'}
        some_list = ['a', 'b']
        dataprocess = DataProcess()
        dataprocess.get_extractor(some_dict)
        self.assertEqual(dataprocess.temp_dict['searchDictionaries'], some_list)

    def test_create_empty_search_dict(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtDataProcessError):
            dataprocess.create()

    # @patch("qtcurate.dataprocess.connect")
    # def test_create(self, con):
    #     mock = Mock()
    #     ex = Extractor()
    #     dataprocess = DataProcess()
    #     dataprocess.add_extractor(ex)
    #     pass

    def test_fetch_dp_id_arg_err(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.fetch(dp_id=[])

    @patch("qtcurate.dataprocess.connect")
    def test_fetch(self, con):
        some_id = 'some id'
        some_dict = {"key": "value"}
        dp = DataProcess()
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_dict
        con.return_value = response

        res = dp.fetch(some_id)
        self.assertEqual(res, some_dict)

    def test_update_dp_id_arg_error(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.update(dp_id=[], update_files=["test.txt"])

    def test_update_list_arg_err(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.update(dp_id="some_id", update_files="file")
    #
    @patch("qtcurate.dataprocess.connect")
    def test_update(self, con):
        some_id = 'some id'
        some_dict = {"key": "value"}
        some_list = ["test.txt"]
        dp = DataProcess()
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_dict
        con.return_value = response

        res = dp.update(some_id, some_list)
        self.assertEqual(res, json_to_tuple(some_dict))
    #

    def test_clone_dp_id_arg_err(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.clone(dp_id=[])

    # def test_clone_tag_files_empty(self):
    #     pass

    @patch("qtcurate.dataprocess.connect")
    def test_clone(self, con):
        some_id = 'some id'
        some_dict = {"id": "value"}
        some_list = ['123']
        dp = DataProcess()
        dp.with_documents(some_list)
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_dict
        con.return_value = response

        res = dp.clone(some_id)
        self.assertEqual(res, json_to_tuple(some_dict))

    def test_delete_argument_type_error(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.delete(dp_id=[])

    @patch("qtcurate.dataprocess.connect")
    def test_delete_true(self, con):
        some_id = 'some id'
        dp = DataProcess()
        response = Mock()
        response.status_code = 200
        response.ok = True
        con.return_value = response

        res = dp.delete(some_id)
        self.assertEqual(res, True)

    @patch("qtcurate.dataprocess.connect")
    def test_delete_false(self, con):
        some_id = 'some id'
        dp = DataProcess()
        response = Mock()
        response.status_code = 200
        response.ok = False
        con.return_value = response

        res = dp.delete(some_id)
        self.assertEqual(res, False)
    #
    def test_progress_argument_type_error(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.progress(dp_id=[])

    @patch("qtcurate.dataprocess.connect")
    def test_progress(self, con):
        some_id = 'some id'
        some_dict = {"key": "value"}
        dp = DataProcess()
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_dict
        con.return_value = response

        res = dp.progress(some_id)
        self.assertEqual(res, json_to_tuple(some_dict))

    # test for wait for completion!!!

    def test_search_dp_id_arg(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.search(dp_id=123)

    def test_search_param_from_arg_error(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.search(dp_id="some_dp", param_from="123")

    def test_search_size_range_arg(self):
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.search(dp_id="some_dp", param_from=5, size=201)

    def test_search_size_not_int_arg(self):
        dp_id = "test"
        param_from = 5
        size = "test"
        dataprocess = DataProcess()
        with self.assertRaises(QtArgumentError):
            dataprocess.search(dp_id, param_from, size)

    def test_search_pairs_arg(self):
        index = "test"
        param_from = 5
        size = 100
        dataprocess = DataProcess()
        f1 = "string"
        with self.assertRaises(QtArgumentError):
            dataprocess.search(index, param_from, size, f1)

    @patch("qtcurate.dataprocess.connect")
    def test_search(self, con):
        some_id = 'some id'
        some_dict = {"key": "value"}
        dp = DataProcess()
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_dict
        con.return_value = response

        res = dp.search(some_id)
        self.assertEqual(res, some_dict)

    @patch("qtcurate.dataprocess.connect")
    def test_read(self, con):
        some_list = []
        dp = DataProcess()
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_list
        con.return_value = response

        res = dp.read()
        self.assertEqual(res, some_list)

if __name__ == '__main__':
    main()
