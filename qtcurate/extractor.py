from __future__ import annotations
from enum import Enum
from qtcurate.exceptions import QtArgumentError
from typing import List, Dict


class ChunkMode(Enum):
    NONE = "NONE"
    SENTENCE = "SENTENCE"
    PAGE = "PAGE"


class SearchMode(Enum):
    ORDERED_SPAN = "ORDERED_SPAN"
    FUZZY_ORDERED_SPAN = "FUZZY_ORDERED_SPAN"
    SPAN = "SPAN"
    FUZZY_SPAN = "FUZZY_SPAN"
    PARTIAL_SPAN = "PARTIAL_SPAN"
    PARTIAL_FUZZY_SPAN = "PARTIAL_FUZZY_SPAN"


class AnalyzeMode(Enum):
    EXACT = "EXACT"
    EXACT_CI = "EXACT_CI"
    WHITESPACE = "WHITESPACE"
    SIMPLE = "SIMPLE"
    STANDARD = "STANDARD"
    LETTER = "LETTER"
    STEM = "STEM"


class Type(Enum):
    LONG = "LONG"
    DATETIME = "DATETIME"
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
        self.mode = None
        self.search_mode = None
        self.analyze_mode = None
        self.type = None
        self.vocab_id = None
        self.vocab_value_type = None
        self.between_values = None
        self.stop_word_list = None
        self.synonym_list = None
        self.data_type = None

    def __repr__(self):
        return f"{self.validator} {self.mode}, {self.type}, {self.vocab_id}, {self.vocab_value_type} {self.data_type}"

    def create_mode(self, analyze_mode: AnalyzeMode, search_mode: SearchMode) -> Extractor:
        if analyze_mode == "SIMPLE" and search_mode == "SPAN":
            self.mode = Mode.UNORDERED
        elif analyze_mode == "STEM" and search_mode == "ORDERED_SPAN":
            self.mode = Mode.STEM.value
        elif analyze_mode == "STEM" and search_mode == "SPAN":
            self.mode - Mode.UNORDERED_STEM
        elif analyze_mode == "STEM" and search_mode == "FUZZY_SPAN":
            self.mode = Mode.FUZZY_UNORDERED_STEM
        else:
            self.mode = Mode.SIMPLE
        return self

    def set_search_mode(self, search_mode: SearchMode) -> Extractor:
        self.search_mode = search_mode
        return self

    def get_search_mode(self) -> SearchMode:
        return self.search_mode

    def get_analyze_mode(self) -> AnalyzeMode:
        return self.analyze_mode

    def set_analyze_mode(self, analyze_mode: AnalyzeMode):
        self.analyze_mode = analyze_mode

    def set_mode(self, mode: Mode) -> Extractor:
        self.mode = mode
        return self

    def get_mode(self) -> Mode:
        return self.mode

    def set_vocabulary(self, vocabulary: str) -> Extractor:
        if isinstance(vocabulary, str):
            self.vocab_id = vocabulary
        else:
            raise QtArgumentError("Argument type error: String is expected as vocab_id")
        return self

    def get_vocab_id(self) -> str:
        return self.vocab_id

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

    def set_type(self, data_type: Type) -> Extractor:
        if isinstance(data_type, Type):
            self.type = data_type
        else:
            raise QtArgumentError("Argument type error: String is expected as qt_type")
        return self

    def get_type(self) -> Type:
        return self.type

    def set_stop_word_list(self, stop_word_list: List) -> Extractor:
        if isinstance(stop_word_list, list):
            self.stop_word_list = stop_word_list
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
            self.vocab_value_type = "REGEX"
        else:
            raise QtArgumentError("Argument type error: String is expected as validator")
        return self

    def get_validator(self) -> str:
        return self.validator
