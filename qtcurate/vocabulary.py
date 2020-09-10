from __future__ import annotations
from qtcurate.qt import Qt
import json
import os.path
from typing import Dict, List, Union, Tuple
from qtcurate.exceptions import QtArgumentError, QtVocabularyError
from qtcurate.utilities import connect, json_to_tuple

dic_entries = "entries"
dic_name = "name"


class Vocabulary(Qt):
    def __init__(self):
        self.headers = {"X-API-Key": Qt.api_key}
        self.temp_dictionary = dict()
        self.temp_dictionary[dic_entries] = []
        self.temp_dictionary[dic_name] = None
        self.id = None
        self.input_stream = None
        self.url = f"{Qt.url}dictionaries/"

    def __repr__(self):
        return str({'name': self.temp_dictionary[dic_name], 'entries': self.temp_dictionary[dic_entries]})

    def get_id(self) -> str:
        return str(self.id)

    def name(self, name: str) -> Vocabulary:
        """Create a new name for dictionary"""
        if isinstance(name, str):
            self.temp_dictionary[dic_name] = name
        else:
            raise QtArgumentError("Argument type error: String is expected as name")
        return self

    def entries(self, entry: Dict) -> Vocabulary:
        """Create dictionary data"""
        if not isinstance(entry, Dict):
            raise QtArgumentError("Argument type error: QtDict is expected as entry")
        elif len(entry) > 2 or len(entry) == 0:
            raise QtArgumentError("Argument error: QtDict must have 1 or 2 elements where keys are 'str' and "
                                  "optional 'category'."
                                  "Example {'str': 'some str', 'category': 'some category'} or just {'str':'some str'}")
        elif "str" not in entry.keys():
            raise QtArgumentError("Argument error: QtDict must have 1 or 2 elements where keys are 'str' and "
                                  "optional 'category'."
                                  "Example {'str': 'some str', 'category': 'some category'} or just {'str':'some str'}")
        elif len(set(entry.keys()).difference({"str", "category"})) != 0:
            raise QtArgumentError("Argument error: QtDict must have 1 or 2 elements where keys are 'str' and "
                                  "optional 'category'."
                                  "Example {'str': 'some str', 'category': 'some category'} or just {'str':'some str'}")
        else:
            self.temp_dictionary[dic_entries].append(entry)
        return self

    def clear(self) -> None:
        """Remove all temporary data"""

        self.temp_dictionary[dic_entries] = []
        self.temp_dictionary[dic_name] = None
        self.id = None
        self.input_stream = None

    def add_entry(self, str_key: Union[str, int, float], category: Union[str, int, float] = None) -> None:
        """Create dictionary data"""
        has_category = False
        if category is not None:
            has_category = True
        if not isinstance(str_key, (str, int, float)):
            raise QtArgumentError("Argument type error: String, integer or float are expected as key")
        elif not isinstance(category, (str, int, float)) and has_category:
            raise QtArgumentError("Argument type error: String, integer or float is expected as value")
        else:
            if has_category:
                self.temp_dictionary[dic_entries].append({'str': str_key, 'category': category})
            else:
                self.temp_dictionary[dic_entries].append({'str': str_key})
        return self

    def read(self) -> List:
        """List all dictionaries"""
        res = connect("get", self.url, self.headers)
        return res.json()

    def fetch(self, qt_id: str) -> Dict:
        """Fetch dictionary by ID"""

        if not isinstance(qt_id, str):
            raise QtArgumentError("Argument type error: String is expected as qt_id")

        res = connect("get", f"{self.url}{qt_id}", self.headers)
        return json_to_tuple(res.json())


    def delete(self, qt_id: str) -> bool:
        """Delete existing dictionary"""

        if not isinstance(qt_id, str):
            raise QtArgumentError("Argument type error: String is expected as qt_id")
        res = connect("delete", f"{self.url}{qt_id}", self.headers)

        return res.ok

    def source(self, file: str) -> Vocabulary:
        if not isinstance(file, str):
            raise QtArgumentError("Argument type error: String is expected as file")
        extension = os.path.splitext(file)[1].lower()
        if extension != ".tsv":
            raise QtArgumentError("Argument type error: TSV file expected")
        if not os.path.exists(file):
            raise QtArgumentError(f"Argument error: File {file} does not exist")
        self.input_stream = file
        return self

    def create(self) -> Dict:
        """Create dictionary data"""

        if self.temp_dictionary[dic_name] is None:
            raise QtVocabularyError("QtDict error: Please add name using name function")

        if self.input_stream is None:
            self.headers['Content-Type'] = 'application/json'
            if len(self.temp_dictionary[dic_entries]) == 0:
                raise QtVocabularyError("QtDict error: Please add dictionary using add_entry function")
            data = {'name': self.temp_dictionary[dic_name], 'entries': self.temp_dictionary[dic_entries]}
            res = connect("post", self.url, self.headers, "data", json.dumps(data))
            self.id = res.json()["id"]
            return json_to_tuple(res.json())
        else:
            files = {
                'name': (None, self.temp_dictionary[dic_name]),
                'file': open(self.input_stream, 'rb')
            }
            res = connect("post", f"{self.url}upload", self.headers, "files", files)
            self.id = res.json()["id"]
            return json_to_tuple(res.json())

    def update(self, qt_id: str) -> Tuple:
        """Update existing dictionary"""
        self.headers['Content-Type'] = 'application/json'
        if not isinstance(qt_id, str):
            raise QtArgumentError("Argument type error: String is expected as qt_id")
        if self.temp_dictionary[dic_name] is None:
            raise QtVocabularyError("QtDict error: Please add name using name function")
        if len(self.temp_dictionary[dic_entries]) == 0:
            raise QtVocabularyError("QtDict error: Please add dictionary using add_entry function")
        data = {'name': self.temp_dictionary[dic_name], 'entries': self.temp_dictionary[dic_entries]}
        res = connect("put", f"{self.url}{qt_id}", self.headers, "data", json.dumps(data))
        del self.headers['Content-Type']

        return json_to_tuple(res.json())
