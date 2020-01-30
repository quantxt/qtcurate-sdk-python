from config import BASE_URL
import requests
import json
from enum import Enum
import os.path
from qt.exceptions import QTFileTypeError, QTArgumentError, QTConnectionError, QTRestApiError, QTTaggingError

url = BASE_URL + "search/"


class DictionaryType(Enum):
    NUMBER = "DOUBLE"
    STRING = "STRING"
    DATETIME = "DATETIME"
    NONE = "NONE"


class Tagging:

    def __init__(self, api_key):
        self.s = requests.Session()
        self.headers = {"X-API-Key": api_key}
        self.d = dict()
        self.d['files'] = []
        self.d['urls'] = []
        self.d['title'] = None
        self.d['index'] = None
        self.d['autotag'] = None
        self.d['maxTokenPerUtt'] = None
        self.d['minTokenPerUtt'] = None
        self.d['exclude_utt_without_entities'] = None
        self.d['searchDictionaries'] = []

    def title(self, value: str):
        """Create title for mining data"""
        if isinstance(value, str):
            self.d['title'] = value
        else:
            raise QTArgumentError("Argument type error: String is expected as title")

    def index(self, value: str):
        """Create index for mining data, this is optional parameter"""
        if isinstance(value, (str, int)):
            self.d['index'] = value
        else:
            raise QTArgumentError("Argument type error: String is expected as index")

    def autotag(self, value: bool):
        """Set autotag for mining data, this is optional parameter"""
        if isinstance(value, bool):
            self.d['autotag'] = value
        else:
            raise QTArgumentError("Argument type error: Boolean is expected as autotag")

    def max_token_per_utt(self, value: int):
        """Create  max token per utt for mining data, this is optional parameter"""
        if isinstance(value, int):
            self.d['maxTokenPerUtt'] = value
        else:
            raise QTArgumentError("Argument type error: Integer is expected as max token per utt")

    def min_token_per_utt(self, value: int):
        """Create min token per utt for mining data, this is optional parameter"""
        if isinstance(value, int):
            self.d['minTokenPerUtt'] = value
        else:
            raise QTArgumentError("Argument type error: Integer is expected as min token per utt")

    def exclude_utt_without_entities(self, value: bool):
        """Set exclude utt for mining data, this is optional parameter"""
        if isinstance(value, bool):
            self.d['exclude_utt_without_entities'] = value
        else:
            raise QTArgumentError("Argument type error: Boolean is expected as exclude utt without entities")

    def files(self, list_of_files: list):
        """Create a list of existing files"""
        if isinstance(list_of_files, list):
            self.d['files'] = list_of_files
        else:
            raise QTArgumentError("Argument type error: Expected list of file indexes")

    def urls(self, list_of_urls: list):
        """Create a list of existing files"""
        if isinstance(list_of_urls, list):
            self.d['urls'] = list_of_urls
        else:
            raise QTArgumentError("Argument type error: Expected list of urls")

    def search_rule(self, dictionary_path: str, vocab_value_type: DictionaryType):
        vocab_dict = dict()
        if isinstance(dictionary_path, str):
            vocab_dict["vocabPath"] = dictionary_path
        else:
            raise QTArgumentError("Argument type error: String is expected as dictionary_path index")
        if isinstance(vocab_value_type, DictionaryType):
            vocab_dict["vocabValueType"] = vocab_value_type.value
        else:
            raise QTArgumentError("Argument type error: DictionaryType object is expected as vocab_value_type")

        self.d['searchDictionaries'].append(vocab_dict)

    def clear(self):
        self.d['files'] = []
        self.d['urls'] = []
        self.d['title'] = None
        self.d['index'] = None
        self.d['autotag'] = None
        self.d['maxTokenPerUtt'] = None
        self.d['minTokenPerUtt'] = None
        self.d['exclude_utt_without_entities'] = None
        self.d['searchDictionaries'] = []

    def upload(self, file: str):
        """Upload files for data mining"""

        if not isinstance(file, str):
            raise QTArgumentError("Argument type error: String is expected as file path")

        extension = os.path.splitext(file)[1].lower()
        if extension not in [".pdf", ".txt", ".html"]:
            raise QTArgumentError("Argument type error: PDF, TXT or HTML file expected")
        if not os.path.exists(file):
            raise QTArgumentError(f"Argument error: File {file} does not exist")
        files = {'file': open(file, 'rb')}
        try:
            res = self.s.post(url+"file", headers=self.headers, files=files)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}")
        return res.json()

    def tagging_files(self):
        """Mine data via dictionaries"""

        self.headers["Content-Type"] = "application/json"
        if len(self.d['files']) == 0:
            raise QTTaggingError("Tagging error: Please add files using files function")
        if len(self.d['searchDictionaries']) == 0:
            raise QTTaggingError("Tagging error: Please add URLs using search_url function")
        data = {'files': self.d['files'], 'searchDictionaries': self.d['searchDictionaries']}
        if len(self.d['searchDictionaries']) != 0:
            data['searchDictionaries'] = self.d['searchDictionaries']
        if self.d['title'] is not None:
            data['title'] = self.d['title']
        if self.d['index'] is not None:
            data['index'] = self.d['index']
        if self.d['autotag'] is not None:
            data['autotag'] = self.d['autotag']
        if self.d['maxTokenPerUtt'] is not None:
            data['maxTokenPerUtt'] = self.d['maxTokenPerUtt']
        if self.d['minTokenPerUtt'] is not None:
            data['minTokenPerUtt'] = self.d['minTokenPerUtt']
        if self.d['exclude_utt_without_entities'] is not None:
            data['exclude_utt_without_entities'] = self.d['exclude_utt_without_entities']
        try:
            res = self.s.post(url+"new", headers=self.headers, data=json.dumps(data))
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}")
        return res.json()

    def delete(self, index: str) -> bool:
        """Delete data container"""

        if not isinstance(index, str):
            raise QTArgumentError("Argument type error: String is expected as index")
        try:
            res = self.s.delete(url + index, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}")
        return res.ok

    def minning_url(self) -> dict:
        """Minning data on URLs"""

        self.headers["Content-Type"] = "application/json"
        if len(self.d['urls']) == 0:
            raise QTTaggingError("Tagging error: Please add urls using files function")
        if len(self.d['searchDictionaries']) == 0:
            raise QTTaggingError("Tagging error: Please add dictionary using search_url function")
        data = {'urls': self.d['urls'], 'searchDictionaries': self.d['searchDictionaries']}
        if self.d['title'] is not None:
            data['title'] = self.d['title']
        if self.d['index'] is not None:
            data['index'] = self.d['index']
        if self.d['autotag'] is not None:
            data['autotag'] = self.d['autotag']
        if self.d['maxTokenPerUtt'] is not None:
            data['maxTokenPerUtt'] = self.d['maxTokenPerUtt']
        if self.d['minTokenPerUtt'] is not None:
            data['minTokenPerUtt'] = self.d['minTokenPerUtt']
        if self.d['exclude_utt_without_entities'] is not None:
            data['exclude_utt_without_entities'] = self.d['exclude_utt_without_entities']
        try:
            res = self.s.post(url + "new", data=json.dumps(data), headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}")
        return res.json()

    def progress(self, index=None):
        """Show progress for submitted data minining job"""

        url_path = "progress"
        if index is not None:
            if isinstance(index, str):
                url_path = url_path + "/" + index
            else:
                raise QTArgumentError("Expected string")
        try:
            status = self.s.get(url + url_path, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if status.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {status.status_code}")
        return status.json()

    def search(self, index: str, param_from=0, size=None, f1=None, f2=None):
        """Search full-text and faceted search"""

        if not isinstance(index, str):
            raise QTArgumentError("Argument type error: String is expected as index")
        if isinstance(param_from, int):
            parameters = [('from', param_from)]
        else:
            raise QTArgumentError("Argument type error: Integer is expected as parameter")
        if size is not None:
            if isinstance(size, int) and 0 < size <= 200:
                parameters.append(('size', size))
            else:
                raise QTArgumentError("Argument type error: Integer between 0 and 200 is expected as parameter")
        if f1 is not None and f2 is not None:
            parameters.append(('f', f1))
            parameters.append(('f', f2))
        elif f1 is None and f2 is None:
            pass
        else:
            raise QTArgumentError("Argument error: Query filters must be used in pairs")
        try:
            res = self.s.get(url + index, headers=self.headers, params=parameters)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}")
        return res.json()

    def report_to_xlsx(self, index: str, path: str):
        """Exporting in Excel format"""

        if not isinstance(index, str):
            raise QTArgumentError("Argument type error: String is expected as index")
        if not isinstance(path, str):
            raise QTArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QTArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".xlsx":
            raise QTFileTypeError("File type error: Please use xlsx extension saving file")
        try:
            report = self.s.get(BASE_URL + "reports/" + index + "/xlsx", headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if report.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {report.status_code}")
        with open(path, 'wb') as excel_file:
            excel_file.write(report.content)
        return report.ok

    def report_to_json(self, index: str, path: str) -> bool:
        """Exporting in Excel format"""

        if not isinstance(index, str):
            raise QTArgumentError("Argument type error: String is expected as index")
        if not isinstance(path, str):
            raise QTArgumentError("Argument type error: String is expected as path")
        directory = os.path.dirname(path)
        if len(directory) == 0:
            directory = "."
        if not (os.access(directory, os.W_OK) and os.access(directory, os.X_OK)):
            raise QTArgumentError("Argument error: No write permission")
        extension = os.path.splitext(path)[1].lower()
        if extension != ".json":
            raise QTFileTypeError("File type error: Please use json extension saving file")
        try:
            report = self.s.get(BASE_URL + "reports/" + index + "/json", headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if report.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {report.status_code}")
        with open(path, "w") as json_file:
            json.dump(report.json(), json_file)
        return report.ok
