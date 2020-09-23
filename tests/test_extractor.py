from unittest import TestCase
from qtcurate.exceptions import *
from qtcurate.extractor import Extractor, SearchMode, AnalyzeMode, Mode, Type


class TestExtractor(TestCase):

    def test_create_mode_unordered(self):
        ex = Extractor()
        some_analyze_mode = AnalyzeMode.SIMPLE
        some_search_mode = SearchMode.SPAN
        some_mode = Mode.UNORDERED
        ex.create_mode(some_analyze_mode, some_search_mode)
        self.assertEqual(ex.mode, some_mode)

    def test_create_mode_stem(self):
        ex = Extractor()
        some_analyze_mode = AnalyzeMode.STEM
        some_search_mode = SearchMode.ORDERED_SPAN
        some_mode = Mode.STEM
        ex.create_mode(some_analyze_mode, some_search_mode)
        self.assertEqual(ex.mode, some_mode)

    def test_create_mode_unordered_stem(self):
        ex = Extractor()
        some_analyze_mode = AnalyzeMode.STEM
        some_search_mode = SearchMode.SPAN
        some_mode = Mode.UNORDERED_STEM
        ex.create_mode(some_analyze_mode, some_search_mode)
        self.assertEqual(ex.mode, some_mode)

    def test_create_mode_fuzzy_unordered_stem(self):
        ex = Extractor()
        some_analyze_mode = AnalyzeMode.STEM
        some_search_mode = SearchMode.FUZZY_SPAN
        some_mode = Mode.FUZZY_UNORDERED_STEM
        ex.create_mode(some_analyze_mode, some_search_mode)
        self.assertEqual(ex.mode, some_mode)

    def test_create_mode_simple(self):
        ex = Extractor()
        some_analyze_mode = AnalyzeMode.WHITESPACE
        some_search_mode = SearchMode.FUZZY_SPAN
        some_mode = Mode.SIMPLE
        ex.create_mode(some_analyze_mode, some_search_mode)
        self.assertEqual(ex.mode, some_mode)

    def test_set_mode(self):
        ex = Extractor()
        some_mode = Mode.SIMPLE
        ex.set_mode(some_mode)
        self.assertEqual(ex.get_mode(), some_mode)

    def test_get_mode(self):
        ex = Extractor()
        some_mode = Mode.SIMPLE
        self.assertEqual(ex.get_mode(), some_mode)

    def test_set_vocabulary(self):
        some_vocab_id = 'some_id'
        ex = Extractor()
        ex.set_vocabulary(some_vocab_id)
        self.assertEqual(ex.vocab_id, some_vocab_id)

    def test_set_vocabulary_arg_err(self):
        ex = Extractor()
        some_vocab_id = []
        with self.assertRaises(QtArgumentError):
            ex.set_vocabulary(some_vocab_id)

    def test_get_vocab_id(self):
        ex = Extractor()
        some_vocab_id = None
        self.assertEqual(ex.get_vocab_id(), some_vocab_id)

    def test_get_vocab_value_type(self):
        ex = Extractor()
        some_vocab_value_type = None
        self.assertEqual(ex.get_vocab_value_type(), some_vocab_value_type)

    def test_set_between_values_arg_err(self):
        be_value = 123
        ex = Extractor()
        with self.assertRaises(QtArgumentError):
            ex.set_between_values(be_value)

    def test_set_between_values(self):
        be_value = '123'
        ex = Extractor()
        self.assertEqual(ex.set_between_values(be_value).between_values, be_value)

    def test_get_between_values(self):
        be_value = None
        ex = Extractor()
        self.assertEqual(ex.get_between_values(), be_value)

    def test_set_type_arg_err(self):
        some_type = '123'
        ex = Extractor()
        with self.assertRaises(QtArgumentError):
            ex.set_type(some_type)

    def test_set_type(self):
        some_type = Type.DATETIME
        ex = Extractor()
        self.assertEqual(ex.set_type(some_type).type, some_type)

    def test_get_type(self):
        ex = Extractor()
        some_type = None
        self.assertEqual(ex.get_type(), some_type)

    def test_set_stop_word_list(self):
        some_swl = [1, 2, 3]
        ex = Extractor()
        self.assertEqual(ex.set_stop_word_list(some_swl).stop_word_list, some_swl)

    def test_set_stop_word_list_arg_err(self):
        some_swl = '123'
        ex = Extractor()
        with self.assertRaises(QtArgumentError):
            ex.set_stop_word_list(some_swl)

    def test_get_stop_word_list(self):
        ex = Extractor()
        self.assertEqual(ex.get_stop_word_list(), None)

    def test_set_synonym_list_arg_err(self):
        some_sl = '123'
        ex = Extractor()
        with self.assertRaises(QtArgumentError):
            ex.set_synonym_list(some_sl)

    def test_set_synonym_list(self):
        some_sl = [1, 2, 3]
        ex = Extractor()
        self.assertEqual(ex.set_synonym_list(some_sl).synonym_list, some_sl)

    def test_get_synonym_list(self):
        ex = Extractor()
        self.assertEqual(ex.get_synonym_list(), None)

    def test_set_validator(self):
        some_validator = '123'
        ex = Extractor()
        self.assertEqual(ex.set_validator(some_validator).validator, some_validator)

    def test_set_validator_re(self):
        some_validator = '123'
        ex = Extractor()
        self.assertEqual(ex.set_validator(some_validator).vocab_value_type, 'REGEX')

    def test_set_validator_arg_err(self):
        some_validator = [1, 2, 3]
        ex = Extractor()
        with self.assertRaises(QtArgumentError):
            ex.set_validator(some_validator)

    def test_get_validator(self):
        ex = Extractor()
        self.assertEqual(ex.get_validator(), None)
