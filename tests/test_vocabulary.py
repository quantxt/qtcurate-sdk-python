import os
from unittest import TestCase, main
from qtcurate.vocabulary import Vocabulary
from qtcurate.exceptions import *
from unittest.mock import Mock, patch


class TestVocabulary(TestCase):

    # Testing get_id method
    def test_get_id(self):
        vocabulary = Vocabulary()
        some_id = None
        self.assertEqual(vocabulary.get_id(), str(some_id))

    # Testing set_id method
    def test_set_id_arg_err(self):
        vocabulary = Vocabulary()
        some_id = 123
        with self.assertRaises(QtArgumentError):
            vocabulary.set_id(some_id)

    def test_set_id(self):
        vocabulary = Vocabulary()
        some_id = 'some id'
        vocabulary.set_id(some_id)
        self.assertEqual(vocabulary.id, some_id)

    # Testing name method
    def test_name_name(self):
        name = "some name"
        vocabulary = Vocabulary()
        vocabulary.name(name)
        self.assertEqual(name, vocabulary.temp_vocabulary["name"])

    def test_name_type(self):
        name = 123
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.name(name)

    # Testing get_name method
    def test_get_name(self):
        vocabulary = Vocabulary()
        some_name = None
        self.assertEqual(vocabulary.temp_vocabulary["name"], some_name)

    # Testing entries method
    def test_entries_type(self):
        test_vocabulary = "string"
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.entries(test_vocabulary)

    def test_entries_vocabulary_len_3(self):
        test_vocabulary = {"str": "str", "category": "category", "some_key": "some_value"}
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.entries(test_vocabulary)

    def test_entries_vocabulary_len_0(self):
        test_vocabulary = {}
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.entries(test_vocabulary)

    def test_entries_vocabulary_content(self):
        test_vocabulary = {"test": "str", "category": "category"}
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.entries(test_vocabulary)

    def test_entries_vocabulary_content_2(self):
        test_vocabulary = {"str": "str", "test": "category"}
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.entries(test_vocabulary)

    def test_entries_category_str(self):
        test_vocabulary = {"str": "str", "category": "category"}
        vocabulary = Vocabulary()
        vocabulary.entries(test_vocabulary)
        self.assertEqual([test_vocabulary], vocabulary.temp_vocabulary['entries'])

    def test_entries_category(self):
        test_vocabulary = {"str": "str"}
        vocabulary = Vocabulary()
        vocabulary.entries(test_vocabulary)
        self.assertEqual([test_vocabulary], vocabulary.temp_vocabulary['entries'])

    # Testing add_entry method
    def test_add_entry(self):
        key = "New York"
        value = "Knicks"
        list_entries = [{"str": key, "category": value}]
        vocabulary = Vocabulary()
        vocabulary.add_entry(key, value)
        self.assertEqual(list_entries, vocabulary.temp_vocabulary['entries'])

    def test_add_entry_key_type(self):
        key = ["test"]
        value = "Knicks"
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.add_entry(key, value)

    def test_add_entry_value_type(self):
        key = "test"
        value = ["Knicks"]
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.add_entry(key, value)

    def test_add_entry_value_none(self):
        key = "test"
        value = None
        list_entries = [{"str": key}]
        vocabulary = Vocabulary()
        vocabulary.add_entry(key, value)
        self.assertEqual(list_entries, vocabulary.temp_vocabulary['entries'])

    # Testing get_entries method
    def test_get_entries(self):
        vocabulary = Vocabulary()
        some_entry = []
        self.assertEqual(vocabulary.temp_vocabulary["entries"], some_entry)

    # Testing read method
    @patch("qtcurate.vocabulary.connect")
    def test_read(self, con):
        voc = Vocabulary()
        some_json = [{"key": "value"}]
        response = Mock()
        response.status_code = 200
        response.json.return_value = some_json
        con.return_value = response
        res = voc.read()
        self.assertEqual(res, some_json)

    # Testing fetch method
    def test_fetch_arg(self):
        vocabulary_id = 123
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.fetch(vocabulary_id)

    @patch("qtcurate.vocabulary.connect")
    def test_fetch(self, con):
        some_id = 'some id'
        some_json = {"id": "some id", "name": "some name", "entries": "some entries"}
        voc = Vocabulary()
        response = Mock()
        response.json.return_value = some_json
        con.return_value = response
        res = voc.fetch(some_id)
        self.assertEqual(str(res), str(some_json))

    # Testing delete method
    def test_delete_arg(self):
        vocabulary_id = 123
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.delete(vocabulary_id)

    @patch("qtcurate.vocabulary.connect")
    def test_delete_true(self, con):
        some_id = 'some id'
        voc = Vocabulary()
        response = Mock()
        response.status_code = 200
        response.ok = True
        con.return_value = response
        res = voc.delete(some_id)
        self.assertEqual(res, True)

    @patch("qtcurate.vocabulary.connect")
    def test_delete_false(self, con):
        some_id = 'some id'
        voc = Vocabulary()
        response = Mock()
        response.status_code = 200
        response.ok = False
        con.return_value = response
        res = voc.delete(some_id)
        self.assertEqual(res, False)

    # Testing source method
    def test_source_arg_file_type(self):
        file = 123
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.source(file)

    def test_source_file_extension(self):
        file = "path"
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.source(file)

    def test_source_file_exist(self):
        file = "path.tsv"
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.source(file)

    def test_source(self):
        pass

    # Testing create method
    def test_create_miss_name(self):
        entries = {"str": "str", "category": "category"}
        vocabulary = Vocabulary()
        vocabulary.entries(entries)
        with self.assertRaises(QtVocabularyError):
            vocabulary.create()

    def test_create_miss_entry(self):
        name = "some name"
        voc = Vocabulary()
        voc.name(name)
        with self.assertRaises(QtVocabularyError):
            voc.create()

    @patch('qtcurate.vocabulary.connect')
    def test_create_input_stream_none(self, con):
        name = "some name"
        some_dict = {"id": "some value", 'name': 'some name', 'entries': [{'str': 'some entry'}]}
        some_entry = "some entry"
        voc = Vocabulary()
        voc.name(name)
        voc.add_entry(some_entry)
        response = Mock()
        response.json.return_value = some_dict
        con.return_value = response
        res = voc.create()
        self.assertEqual(str(res), str(some_dict))

    @patch('qtcurate.vocabulary.connect')
    def test_create_input_stream(self, con):
        name = "some name"
        some_tsv_file = 'test.tsv'
        with open(some_tsv_file, "w") as f:
            f.write("Delete me!")
        some_dict = {"id": "some value", 'name': 'some name', 'entries': [{'str': 'some entry'}]}
        some_entry = "some entry"
        voc = Vocabulary()
        voc.name(name)
        voc.add_entry(some_entry)
        voc.source(some_tsv_file)
        response = Mock()
        response.json.return_value = some_dict
        con.return_value = response
        res = voc.create()
        self.assertEqual(str(res), str(some_dict))
        os.remove("test.tsv")

    # Testing update method
    def test_update_arg_type(self):
        vocabulary_id = 123
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.update(vocabulary_id)

    def test_update_name(self):
        vocabulary_id = "string"
        entries = {"str": "str", "category": "category"}
        vocabulary = Vocabulary()
        vocabulary.entries(entries)
        with self.assertRaises(QtVocabularyError):
            vocabulary.update(vocabulary_id)

    def test_update_entries(self):
        vocabulary_id = "string"
        name = "name"
        vocabulary = Vocabulary()
        vocabulary.name(name)
        with self.assertRaises(QtVocabularyError):
            vocabulary.update(vocabulary_id)

    @patch("qtcurate.vocabulary.connect")
    def test_update(self, con):
        some_id = "some id"
        some_name = 'some name'
        some_key = 'some key'
        some_dict = {"id": None, 'name': 'some name', 'entries': [{'str': 'some entry'}]}
        voc = Vocabulary()
        voc.name(some_name)
        voc.add_entry(some_key)
        response = Mock()
        response.json.return_value = some_dict
        con.return_value = response
        res = voc.update(some_id)
        self.assertEqual(str(res), str(some_dict))


if __name__ == '__main__':
    main()
