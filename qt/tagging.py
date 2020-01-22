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
            raise QTArgumentError("Expected string")

    def index(self, value: str):
        """Create index for mining data, this is optional parameter"""
        if isinstance(value, str):
            self.d['index'] = value
        else:
            raise QTArgumentError("Expected string")

    def autotag(self, value: bool):
        """Set autotag for mining data, this is optional parameter"""
        if isinstance(value, bool):
            self.d['autotag'] = value
        else:
            raise QTArgumentError("Expected boolean")

    def max_token_per_utt(self, value: int):
        """Create  max token per utt for mining data, this is optional parameter"""
        if isinstance(value, int):
            self.d['maxTokenPerUtt'] = value
        else:
            raise QTArgumentError("Expected integer")

    def set_min_token_per_utt(self, value: int):
        """Create min token per utt for mining data, this is optional parameter"""
        if isinstance(value, int):
            self.d['minTokenPerUtt'] = value
        else:
            raise QTArgumentError("Expected integer")

    def exclude_utt_without_entities(self, value: bool):
        """Set exclude utt for mining data, this is optional parameter"""
        if isinstance(value, bool):
            self.d['exclude_utt_without_entities'] = value
        else:
            raise QTArgumentError("Expected boolean")

    def files(self, list_of_files: list):
        """Create a list of existing files"""
        if isinstance(list_of_files, list):
            self.d['files'] = list_of_files
        else:
            raise QTArgumentError("Expected list")

    def urls(self, list_of_urls: list):
        """Create a list of existing files"""
        if isinstance(list_of_urls, list):
            self.d['urls'] = list_of_urls
        else:
            raise QTArgumentError("Expected list")

    def search_rule(self, dictionary_path: str, vocal_value_type: DictionaryType):
        vocab_dict = dict()
        vocab_dict["vocabPath"] = dictionary_path
        vocab_dict["vocabValueType"] = vocal_value_type.value
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
        extension = os.path.splitext(file)[1].lower()
        try:
            if extension not in ["pdf", "txt", "html"]:
                raise QTFileTypeError("File Type Error. Allowed PDF, TXT and HTML files")
            if not os.path.exists(file):
                raise QTFileTypeError("File Not Exist. Please check your path")
            files = {'file': open(file, 'rb')}
            res = self.s.post(url+"file", headers=self.headers, files=files)
        except requests.exceptions.RequestException as e:
            raise e
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.json()

    def tagging_files(self):
        """Mine data via dictionaries"""
        if len(self.d['files']) == 0:
            raise QTTaggingError("You must add files. Use files function to add new file in list of files")
        if len(self.d['searchDictionaries']) == 0:
            raise QTTaggingError("You must add dictionaries. Use dictionaries function to add new dictionary")
        data = {'files': self.d['files'], 'searchDictionaries': self.d['searchDictionaries']}
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
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.json()

    def delete(self, tag_id: str) -> bool:
        """Delete data container"""
        try:
            res = self.s.delete(url+tag_id, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise e
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.ok

    def minning_url(self) -> dict:
        """Minning data on URLs"""
        if len(self.d['urls']) == 0:
            raise QTTaggingError("You must add urls. Use urls() function to add list of url")
        if len(self.d['searchDictionaries']) == 0:
            raise QTTaggingError("You must add dictionaries. Use dictionaries function to add new dictionary")
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
            print(url + "new")
            res = self.s.post(url + "new", data=json.dumps(data), headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.json()

    def progress(self, index=None):
        """Show progress for submitted data minining job"""
        url_path = "progress"
        if index is not None:
            url_path = url_path + "/" + index
        try:
            status = self.s.get(url + url_path, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if status.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error"
                                 f"{status.status_code}")
        return status.json()

    def search(self, string: str, param_from=0, size=None, f1=None, f2=None):
        """Search full-text and faceted search"""
        try:
            parameters = [('from', param_from)]
            if size is not None:
                parameters.append(('size', size))
            if f1 is not None and f2 is not None:
                parameters.append(('f', f1))
                parameters.append(('f', f1))
            elif f1 is None and f2 is None:
                pass
            else:
                raise QTArgumentError("Filter parameters must be used in pairs")
            res = self.s.get(url + string, headers=self.headers, params=parameters)
        except requests.exceptions.RequestException as e:
            raise e
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.json()

    def report_to_xslx(self, element: str, path: str):
        """Exporting in Excel format"""
        try:
            report = self.s.get(BASE_URL + "reports/" + element + "/xlsx", headers=self.headers)
            with open(path, 'wb') as excel_file:
                excel_file.write(report.content)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        except Exception as e:
            raise QTFileTypeError(e)
        if report.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error"
                                 f"{report.status_code}")
        return report.ok

    def report_to_json(self, element: str, path: str) -> bool:
        """Exporting in Excel format"""
        try:
            report = self.s.get(BASE_URL + "reports/" + element + "/json", headers=self.headers)
            with open(path, "w") as json_file:
                json_file.write(report.content)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        except QTFileTypeError as e:
            raise QTFileTypeError(e)
        if report.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error"
                                 f"{report.status_code}")
        return report.ok
