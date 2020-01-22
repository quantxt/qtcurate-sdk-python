from config import BASE_URL
import requests
import json
import os.path
from typing import Dict
from qt.exceptions import QTFileTypeError, QTArgumentError, QTDictionaryError, QTConnectionError, QTRestApiError, \
    QTDictionaryIdError


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
        self.d['name'] = name

    def entries(self, entries: Dict):
        """Create dictionary data"""
        if isinstance(entries, Dict):
            self.d['entries'].append(entries)
        else:
            raise QTArgumentError("Expected dictionary")

    def clear(self):
        self.d['entries'] = []
        self.d['name'] = None

    def add_entry(self, key, value):
        """Create dictionary data"""
        if not isinstance(key, (str, int, float)):
            raise QTArgumentError("Unexpected key type")
        elif not isinstance(value, (str, int, float)):
            raise QTArgumentError("Unexpected value type")
        self.d['entries'].append({'key': key, 'value': value})

    def list(self) -> Dict:
        """List all dictionaries"""
        try:
            listed = self.s.get(self.url,  headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if listed.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error"
                                 f"{listed.status_code}")
        return listed.json()

    def fetch(self, dict_id: str):
        """Fetch dictionary by ID"""
        if not isinstance(dict_id, str):
            raise QTArgumentError("Expected string")
        try:
            f = self.s.get(self.url+dict_id, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if f.status_code == 401:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error"
                                 f"{f.status_code}")
        elif f.status_code == 404:
            raise QTDictionaryIdError("Operation not succesfull. Resource not found")
        elif f.status_code not in [200, 201]:
            raise QTRestApiError("Unknown error.")

        return f.json()

    def delete(self, dict_id: str) -> bool:
        """Delete existing dictionary"""
        if not isinstance(dict_id, str):
            raise QTArgumentError("Expected string")
        try:
            res = self.s.delete(self.url+dict_id, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code == 401:
            raise QTRestApiError(
                f"Error: Full authentification is required to access this resource. HTTP Error {res.status_code}")
        elif res.status_code == 404:
            raise QTDictionaryIdError("Operation not succesfull. Resource not found")
        return res.ok

    def create(self) -> bool:
        """Create dictionary data"""
        if self.d['name'] is None:
            raise QTDictionaryError("Name must be defined")
        if len(self.d['entries']) == 0:
            raise QTDictionaryError("You must add entries. Use add_entry or entries functions")
        data = {'name': self.d['name'], 'entries': self.d['entries']}
        self.headers['Content-Type'] = 'application/json'
        try:
            created = self.s.post(self.url, headers=self.headers, data=json.dumps(data))
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if created.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{created.status_code}")
        return created.json()

    def update(self, dict_id: str) -> bool:
        """Update existing dictionary"""
        if self.d['name'] is None:
            raise QTDictionaryError("Name must be defined")
        if len(self.d['entries']) == 0:
            raise QTDictionaryError("You must add entries. Use add_entry or entries functions")
        data = {'name': self.d['name'], 'entries': self.d['entries']}
        try:
            updated = self.s.put(self.url+dict_id, headers=self.headers, data=json.dumps(data))
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if updated.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error"
                                 f" {updated.status_code}")
        return updated.ok

    def upload(self, file: str, name: str):
        """Upload dictionary data from TSV files"""
        extension = os.path.splitext(file)[1].lower()
        try:
            if extension != ".tsv":
                raise QTFileTypeError("File Type Error. Allowed only tsv files")
            if not os.path.exists(file):
                raise QTFileTypeError("File Not Exist. Please check your path")
            files = {
                'name': (None, name),
                'file': open(file, 'rb')
            }
            res = self.s.post(self.url+"upload", headers=self.headers, files=files)
        except requests.exceptions.RequestException as e:
            raise e
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.json()

    def __repr__(self):
        return str({'name': self.d['name'], 'entries': self.d['entries']})
