from unittest import TestCase, main
from qtcurate.vocabulary import Vocabulary
from qtcurate.exceptions import *


class TestQtDict(TestCase):

    def test_get_id(self):
        vocabulary = Vocabulary()
        some_id = None
        self.assertEqual(vocabulary.get_id(), str(some_id))

    def test_name_name(self):
        name = "some name"
        vocabulary = Vocabulary()
        vocabulary.name(name)
        self.assertEqual(name, vocabulary.temp_dictionary["name"])

    def test_name_type(self):
        name = 12345
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.name(name)

    def test_entries_type(self):
        test_vocabulary = "string"
        vocabulary = Vocabulary()
        with self.assertRaises(QtArgumentError):
            vocabulary.entries(test_vocabulary)

    def test_entries_dict_len_3(self):
        test_vocabulary = {"str": "str", "category": "category", "some_key": "some_value"}
        dic = Vocabulary()
        with self.assertRaises(QtArgumentError):
            dic.entries(test_vocabulary)

    def test_entries_vocabulary_len_0(self):
        test_vocabulary = {}
        dic = Vocabulary()
        with self.assertRaises(QtArgumentError):
            dic.entries(test_vocabulary)

    def test_entries_vocabulary_content(self):
        test_vocabulary = {"test": "str", "category": "category"}
        dic = Vocabulary()
        with self.assertRaises(QtArgumentError):
            dic.entries(test_vocabulary)

    def test_entries_vocabulary_content_2(self):
        test_vocabulary = {"str": "str", "test": "category"}
        dic = Vocabulary()
        with self.assertRaises(QtArgumentError):
            dic.entries(test_vocabulary)

    def test_entries(self):
        test_vocabulary = {"str": "str", "category": "category"}
        dic = Vocabulary()
        dic.entries(test_vocabulary)
        self.assertEqual([test_vocabulary], dic.temp_dictionary['entries'])

    def test_entries_1(self):
        test_vocabulary = {"str": "str"}
        dic = Vocabulary()
        dic.entries(test_vocabulary)
        self.assertEqual([test_vocabulary], dic.temp_dictionary['entries'])

    def test_add_entry(self):
        key = "New York"
        value = "Knicks"
        list_entries = [{"str": key, "category": value}]
        dic = Vocabulary()
        dic.add_entry(key, value)
        self.assertEqual(list_entries, dic.temp_dictionary['entries'])

    def test_add_entry_key_type(self):
        key = ["test"]
        value = "Knicks"
        dic = Vocabulary()
        with self.assertRaises(QtArgumentError):
            dic.add_entry(key, value)

    def test_add_entry_value_type(self):
        key = "test"
        value = ["Knicks"]
        dic = Vocabulary()
        with self.assertRaises(QtArgumentError):
            dic.add_entry(key, value)

    def test_add_entry_value_none(self):
        key = "test"
        value = None
        list_entries = [{"str": key}]
        dic = Vocabulary()
        dic.add_entry(key, value)
        self.assertEqual(list_entries, dic.temp_dictionary['entries'])

    def test_fetch_arg(self):
        vocabulary_id = 123
        dic = Vocabulary()
        with self.assertRaises(QtArgumentError):
            dic.fetch(vocabulary_id)

    def test_delete_arg(self):
        vocabulary_id = 123
        dic = Vocabulary()
        with self.assertRaises(QtArgumentError):
            dic.delete(vocabulary_id)

    def test_create_miss_name(self):
        entries = {"str": "str", "category": "category"}
        dic = Vocabulary()
        dic.entries(entries)
        with self.assertRaises(QtVocabularyError):
            dic.create()

    def test_create_miss_entry(self):
        name = "some name"
        dic = Vocabulary()
        dic.name(name)
        with self.assertRaises(QtVocabularyError):
            dic.create()

    def test_update_arg_type(self):
        vocabulary_id = 123
        dic = Vocabulary()
        with self.assertRaises(QtArgumentError):
            dic.update(vocabulary_id)

    def test_update_name(self):
        vocabulary_id = "string"
        entries = {"str": "str", "category": "category"}
        dic = Vocabulary()
        dic.entries(entries)
        with self.assertRaises(QtVocabularyError):
            dic.update(vocabulary_id)

    def test_update_entries(self):
        vocabulary_id = "string"
        name = "name"
        dic = Vocabulary()
        dic.name(name)
        with self.assertRaises(QtVocabularyError):
            dic.update(vocabulary_id)

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


if __name__ == '__main__':
    main()
