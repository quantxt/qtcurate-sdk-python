from unittest import TestCase, main
from qtcurate.model import Model
from qtcurate.exceptions import *
from qtcurate.extractor import ChunkMode, Extractor, Type, Mode
from unittest.mock import patch, Mock
from qtcurate.vocabulary import json_to_tuple, connect


class TestModel(TestCase):

    # Test get_id method
    def test_get_id(self):
        some_id = None
        model = Model()
        self.assertEqual(model.get_id(), str(some_id))

    # Test set_id method
    def test_set_id(self):
        model = Model()
        model.set_id('some id')
        self.assertEqual(model.id, 'some id')

    # Test set_chunk method
    def test_set_chunk(self):
        model = Model()
        some_chunk = ChunkMode.SENTENCE
        model.set_chunk(some_chunk)
        self.assertEqual(model.temp_dict["chunk"], some_chunk.value)

    # Test get_uuid method
    def test_get_uuid(self):
        model = Model()
        some_uuid = None
        self.assertEqual(model.get_uuid(), str(some_uuid))

    # Test set_description method
    def test_set_description(self):
        title = "some title"
        model = Model()
        model.set_description(title)
        self.assertEqual(title, model.temp_dict["title"])

    def test_set_description_arg_error(self):
        title = 12
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.set_description(title)

    # Test exclude_utt_without_entities method
    def test_exclude_utt(self):
        value = True
        model = Model()
        model.exclude_utt_without_entities(value)
        self.assertEqual(value, model.temp_dict["excludeUttWithoutEntities"])

    def test_exclude_utt_arg_error(self):
        value = 12
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.exclude_utt_without_entities(value)

    # Test set_workers method
    def test_set_workers_arg_err(self):
        value = '123'
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.set_workers(value)

    def test_set_workers(self):
        value = 123
        model = Model()
        model.set_workers(value)
        self.assertEqual(model.temp_dict["numWorkers"], value)

    # Test with_documents method
    def test_with_documents(self):
        list_files = ["file1", "file2"]
        model = Model()
        model.with_documents(list_files)
        self.assertEqual(list_files, model.temp_dict['files'])

    def test_with_documents_arg_error(self):
        list_files = "string"
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.with_documents(list_files)

    # Test add_extractor method
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

        model = Model()
        model.add_extractor(ex)
        self.assertEqual(model.temp_dict["searchDictionaries"], some_list)

    def test_add_extractor_regex_err(self):
        ex = Extractor()
        ex.set_validator('[')
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.add_extractor(ex)

    # Test get_extractor method
    def test_get_extractor(self):
        some_dict = {'searchDictionaries': 'ab'}
        some_list = ['a', 'b']
        model = Model()
        model.get_extractor(some_dict)
        self.assertEqual(model.temp_dict['searchDictionaries'], some_list)

    def test_create_empty_search_dict(self):
        model = Model()
        with self.assertRaises(QtDataProcessError):
            model.create()

    # Test create method
    @patch("qtcurate.model.connect")
    def test_create(self, con):
        pass

    # Test fetch method
    def test_fetch_model_id_arg_err(self):
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.fetch(model_id=[])

    @patch("qtcurate.model.connect")
    def test_fetch(self, con):
        some_id = 'some id'
        some_dict = {"key": "value"}
        model = Model()
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_dict
        con.return_value = response
        res = model.fetch(some_id)
        self.assertEqual(res, some_dict)

    # Test update method
    def test_update_model_id_arg_error(self):
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.update(model_id=[], update_files=["test.txt"])

    def test_update_list_arg_err(self):
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.update(model_id="some_id", update_files="file")

    @patch("qtcurate.model.connect")
    def test_update(self, con):
        some_id = 'some id'
        some_dict = {"key": "value"}
        some_list = ["test.txt"]
        model = Model()
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_dict
        con.return_value = response

        res = model.update(some_id, some_list)
        self.assertEqual(res, json_to_tuple(some_dict))

    # Test connect method
    def test_clone_model_id_arg_err(self):
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.clone(model_id=[])

    def test_clone_tag_files_empty(self):
        model = Model()
        mod_id = 'some id'
        with self.assertRaises(QtDataProcessError):
            model.clone(mod_id)

    @patch("qtcurate.model.connect")
    def test_clone(self, con):
        some_id = 'some id'
        some_dict = {"id": "value"}
        some_list = ['123']
        model = Model()
        model.with_documents(some_list)
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_dict
        con.return_value = response
        res = model.clone(some_id)
        self.assertEqual(res, json_to_tuple(some_dict))

    # Test delete method
    def test_delete_argument_type_error(self):
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.delete(model_id=[])

    @patch("qtcurate.model.connect")
    def test_delete_true(self, con):
        some_id = 'some id'
        model = Model()
        response = Mock()
        response.status_code = 200
        response.ok = True
        con.return_value = response
        res = model.delete(some_id)
        self.assertEqual(res, True)

    @patch("qtcurate.model.connect")
    def test_delete_false(self, con):
        some_id = 'some id'
        model = Model()
        response = Mock()
        response.status_code = 200
        response.ok = False
        con.return_value = response
        res = model.delete(some_id)
        self.assertEqual(res, False)

    # Test progress method
    def test_progress_argument_type_error(self):
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.progress(model_id=[])

    @patch("qtcurate.model.connect")
    def test_progress(self, con):
        some_id = 'some id'
        some_dict = {"key": "value"}
        model = Model()
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_dict
        con.return_value = response

        res = model.progress(some_id)
        self.assertEqual(res, json_to_tuple(some_dict))

    def test_search_model_id_arg(self):
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.search(model_id=123)

    def test_search_param_from_arg_error(self):
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.search(model_id="some_model", param_from="123")

    def test_search_size_range_arg(self):
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.search(model_id="some_model", param_from=5, size=201)

    def test_search_size_not_int_arg(self):
        model_id = "test"
        param_from = 5
        size = "test"
        model = Model()
        with self.assertRaises(QtArgumentError):
            model.search(model_id, param_from, size)

    def test_search_pairs_arg(self):
        index = "test"
        param_from = 5
        size = 100
        model = Model()
        f1 = "string"
        with self.assertRaises(QtArgumentError):
            model.search(index, param_from, size, f1)

    @patch("qtcurate.model.connect")
    def test_search(self, con):
        some_id = 'some id'
        some_dict = {"key": "value"}
        model = Model()
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_dict
        con.return_value = response
        res = model.search(some_id)
        self.assertEqual(res, some_dict)

    # Test read method
    @patch("qtcurate.model.connect")
    def test_read(self, con):
        some_list = []
        model = Model()
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_list
        con.return_value = response
        res = model.read()
        self.assertEqual(res, some_list)


if __name__ == '__main__':
    main()
