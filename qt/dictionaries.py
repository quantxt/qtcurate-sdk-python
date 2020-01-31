from config import BASE_URL
import requests
import json
import os.path
from typing import Dict
from qt.exceptions import QTArgumentError, QTDictionaryError, QTConnectionError, QTRestApiError


class Dictionary:
    def __init__(self, api_key):
        self.s = requests.Session()
        self.headers = {"X-API-Key": api_key}
        self.d = dict()
        self.d['entries'] = []
        self.d['name'] = None
        self.url = BASE_URL + "dictionaries/"

    def name(self, name: str):
        """Create a new name for dictionary"""

        if isinstance(name, str):
            self.d['name'] = name
        else:
            raise QTArgumentError("Argument type error: String is expected as name")

    def entries(self, entry: Dict):
        """Create dictionary data"""

        if not isinstance(entry, Dict):
            raise QTArgumentError("Argument type error: Dictionary is expected as entry")
        elif len(entry) != 2:
            raise QTArgumentError("Argument error: Dictionary must have 2 element where keys are 'key' and 'value'."
                                  "Example {'key': 'some key', 'value': 'some value'} ")
        elif "key" not in entry.keys() or "value" not in entry.keys():
            raise QTArgumentError("Argument error: Dictionary must have 2 element where keys are 'key' and 'value'."
                                  "Example {'key': 'some key', 'value': 'some value'} ")
        else:
            self.d['entries'].append(entry)



    def clear(self):
        """Set default values"""

        self.d['entries'] = []
        self.d['name'] = None

    def add_entry(self, key, value):
        """Create dictionary data"""

        if not isinstance(key, (str, int, float)):
            raise QTArgumentError("Argument type error: String, integer or float are expected as key")
        elif not isinstance(value, (str, int, float)):
            raise QTArgumentError("Argument type error: String, integer or float is expected as value")
        self.d['entries'].append({'key': key, 'value': value})

    def list(self) -> Dict:
        """List all dictionaries"""

        try:
            listed = self.s.get(self.url,  headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if listed.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {listed.status_code}")
        return listed.json()

    def fetch(self, index: str):
        """Fetch dictionary by ID"""

        if not isinstance(index, str):
            raise QTArgumentError("Argument type error: String is expected as index")
        try:
            f = self.s.get(self.url + index, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if f.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {f.status_code}")
        return f.json()

    def delete(self, index: str) -> bool:
        """Delete existing dictionary"""

        if not isinstance(index, str):
            raise QTArgumentError("Argument type error: String is expected as index")
        try:
            res = self.s.delete(self.url + index, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}")
        return res.ok

    def create(self) -> Dict:
        """Create dictionary data"""

        if self.d['name'] is None:
            raise QTDictionaryError("Dictionary error: Please add name using name function")
        if len(self.d['entries']) == 0:
            raise QTDictionaryError("Dictionary error: Please add dictionary using add_entry function")
        data = {'name': self.d['name'], 'entries': self.d['entries']}
        self.headers['Content-Type'] = 'application/json'
        try:
            created = self.s.post(self.url, headers=self.headers, data=json.dumps(data))
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if created.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {created.status_code}")
        return created.json()

    def update(self, index: str) -> bool:
        """Update existing dictionary"""

        if not isinstance(index, str):
            raise QTArgumentError("Argument type error: String is expected as index")
        if self.d['name'] is None:
            raise QTDictionaryError("Dictionary error: Please add name using name function")
        if len(self.d['entries']) == 0:
            raise QTDictionaryError("Dictionary error: Please add dictionary using add_entry function")
        data = {'name': self.d['name'], 'entries': self.d['entries']}
        try:
            updated = self.s.put(self.url + index, headers=self.headers, data=json.dumps(data))
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if updated.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {updated.status_code}")
        return updated.ok

    def upload(self, file: str, name: str):
        """Upload dictionary data from TSV files"""

        if not isinstance(file, str):
            raise QTArgumentError("Argument type error: String is expected as file")
        if not isinstance(name, str):
            raise QTArgumentError("Argument type error: String is expected as name")
        extension = os.path.splitext(file)[1].lower()
        if extension != ".tsv":
            raise QTArgumentError("Argument type error: TSV file expected")
        if not os.path.exists(file):
            raise QTArgumentError(f"Argument error: File {file} does not exist")
        files = {
            'name': (None, name),
            'file': open(file, 'rb')
        }
        try:
            res = self.s.post(self.url+"upload", headers=self.headers, files=files)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202]:
            raise QTRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}")
        return res.json()
