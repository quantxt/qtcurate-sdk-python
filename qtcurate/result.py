import json
import os
from typing import List
from qtcurate.exceptions import QtArgumentError, QtFileTypeError
from qtcurate.qt import Qt
from qtcurate.utilities import connect, json_to_tuple

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

    def  result_xlsx_exporter(self, path: str) -> None:
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
