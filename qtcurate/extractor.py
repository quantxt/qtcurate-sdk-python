from __future__ import annotations
from enum import Enum
from qtcurate.data_types import SearchMode, AnalyzeMode, DictionaryType
from qtcurate.exceptions import QtArgumentError
from typing import List


class DataType(Enum):
    LONG = "LONG"
    KEYWORD = "KEYWORD"
    DATETIME = "DATETIME"
    STRING = "STRING"
    DOUBLE = "DOUBLE"


class Mode(Enum):
    SIMPLE = "SIMPLE"
    UNORDERED = "UNORDERED"
    STEM = "STEM"
    UNORDERED_STEM = "UNORDERED_STEM"
    FUZZY_UNORDERED_STEM = "FUZZY_UNORDERED_STEM"


class Extractor:

    def __init__(self):
        self.validator = None
        self.mode = Mode.SIMPLE
        self.type = None
        self.vocab_id = None
        self.vocab_value_type = None
        self.between_values = None
        self.stop_word_list = None
        self.synonym_list = None
        self.data_type = None

    def set_data_type(self, data_type: DataType) -> None:
        if isinstance(data_type, DataType) is not None:
            self.data_type = data_type

    def get_data_type(self) -> str:
        return self.data_type.value

    def set_mode(self, analyze_mode: AnalyzeMode, search_mode: SearchMode) -> Extractor:
        if analyze_mode == "SIMPLE" and search_mode == "SPAN":
            self.mode = Mode.UNORDERED
        elif analyze_mode == "STEM" and search_mode == "ORDERED_SPAN":
            self.mode = Mode.STEM
        elif analyze_mode == "STEM" and search_mode == "SPAN":
            self.mode - Mode.UNORDERED_STEM
        elif analyze_mode == "STEM" and search_mode == "FUZZY_SPAN":
            self.mode = Mode.FUZZY_UNORDERED_STEM
        else:
            self.mode = Mode.SIMPLE
        return self

    def get_mode(self) -> str:
        return self.mode.value

    def set_vocabulary(self, vocabulary: str) -> Extractor:
        if isinstance(vocabulary, str):
            self.vocab_id = vocabulary
        else:
            raise QtArgumentError("Argument type error: String is expected as vocab_id")
        return self

    def get_vocab_id(self) -> str:
        return self.vocab_id

    def set_vocab_value_type(self, vocab_value_type: DictionaryType) -> Extractor:
        if isinstance(vocab_value_type, DictionaryType):
            self.vocab_value_type = vocab_value_type.value
        else:
            raise QtArgumentError("Argument type error: DictionaryType object is expected as vocab_value_type")
        return self

    def get_vocab_value_type(self) -> str:
        return self.vocab_value_type

    def set_between_values(self, between_values: str) -> Extractor:
        if isinstance(between_values, str):
            self.between_values = between_values
        else:
            raise QtArgumentError("Argument type error: String is expected as between_values")
        return self

    def get_between_values(self) -> str:
        return self.between_values

    def set_type(self, qt_type: DataType) -> Extractor:
        if isinstance(qt_type, str):
            self.type = qt_type
        else:
            raise QtArgumentError("Argument type error: String is expected as qt_type")
        return self

    def get_type(self) -> DataType:
        return self.type

    def set_stop_word_list(self, stop_word_List: List) -> Extractor:
        if isinstance(stop_word_List, list):
            self.stop_word_list = stop_word_List
        else:
            raise QtArgumentError("Argument type error: List is expected as stop_word_list")
        return self

    def get_stop_word_list(self) -> List:
        return self.stop_word_list

    def set_synonym_list(self, synonym_list: List) -> Extractor:
        if isinstance(synonym_list, list):
            self.synonym_list = synonym_list
        else:
            raise QtArgumentError("Argument type error: List is expected as synonym_list")

        return self

    def get_synonym_list(self) -> List:
        return self.synonym_list

    def set_validator(self, validator: str) -> Extractor:
        if isinstance(validator, str):
            self.validator = validator
        else:
            raise QtArgumentError("Argument type error: String is expected as validator")
        return self

    def get_validator(self) -> str:
        return self.validator
