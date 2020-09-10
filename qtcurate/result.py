import json
import os
from typing import List
from qtcurate.exceptions import QtArgumentError, QtFileTypeError
from qtcurate.qt import Qt
from qtcurate.utilities import connect


class Result:

    def __init__(self, dp_id):
        self.id = dp_id
        self.headers = {"X-API-Key": Qt.api_key}
        self.url = Qt.url

    def raw_exporter(self, path: str) -> None:
        """Exporting in JSON format"""

        if not isinstance(path, str):
            raise QtArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QtArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".json":
            raise QtFileTypeError("File type error: Please use json extension saving file")
        res = connect("get", f"{self.url}reports/{self.id}/json", self.headers)
        with open(path, "w") as json_file:
            json.dump(res.json(), json_file)

    def result_xlsx_exporter(self, path: str) -> None:
        """Exporting in Excel format"""

        if not isinstance(path, str):
            raise QtArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QtArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".xlsx":
            raise QtFileTypeError("File type error: Please use xlsx extension saving file")
        res = connect("get", f"{self.url}reports/{self.id}/xlsx", self.headers)

        with open(path, 'wb') as excel_file:
            excel_file.write(res.content)

    def read(self) -> List:
        """Convert to Object namedtuple"""

        res = connect("get", f"{self.url}reports/{self.id}/json", self.headers)
        return res.json()


class Field:
    def __init__(self, result: List):
        self.search_id = result["searchId"]
        if "title" in result:
            self.title = result["title"]
        else:
            self.title = ""
        if "source" in result:
            self.source = result["source"]
        else:
            self.source = ""
        if "link" in result:
            self.link = result["link"]
        else:
            self.link = ""
        if "date" in result:
            self.date = result["date"]
        else:
            self.date = ""
        if "position" in result:
            self.position = result["position"]
        else:
            self.position = ""
        if "values" in result:
            self.values = result["values"]
        else:
            self.values = ""

    def __repr__(self):
        return f"{self.search_id}, {self.source}, {self.values}"

    def get_id(self):
        return self.search_id

    def get_title(self):
        return self.title

    def get_source(self):
        return self.source

    def get_link(self):
        return self.source

    def get_date(self):
        return self.date

    def get_position(self):
        return self.position

    def get_values(self):
        return self.values


class FieldValues:

    def __init__(self, values: List):
        self.vocab_name = []
        self.vocab_id = []
        self.category = []
        self.type = []
        self.str = []
        if values is not None:
            for value in values:
                if "dict_name" in value:
                    self.vocab_name.append(value["dict_name"])
                if "dict_id" in value:
                    self.vocab_id.append(value["dict_id"])
                if "category" in value:
                    self.category.append(value["category"])
                if "type" in value:
                    self.type.append(value["type"])
                if "str" in value:
                    self.str.append(value["str"])

    def __repr__(self):
        return f"{self.vocab_name}, {self.str}"

    def get_vocab_id(self) -> List:
        return self.vocab_id

    def get_vocab_name(self) -> List:
        return self.vocab_name

    def get_category(self) -> List:
        return self.category

    def get_str(self) -> List:
        return self.str

    def get_type(self) -> str:
        return self.type
