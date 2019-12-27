from config import BASE_URL
import requests
import json
import os.path
from qt.exceptions import QTFileTypeError, QTArgumentError, QTConnectionError, QTRestApiError, QTDictionaryError


class Tagging:
    def __init__(self, api_key):
        self.s = requests.Session()
        self.headers = {"X-API-Key": api_key}
        self.url = BASE_URL + "search/"
        self.d = dict()
        self.d['files'] = []
        self.d['dictionaries'] = []
        self.d['urls'] = []

    def title(self, title: str):
        """Create title for mining data"""
        self.d['title'] = title

    def files(self, list_of_files: list):
        """Create a list of existing files"""
        if isinstance(list_of_files, list):
            self.d['files'] = list_of_files
        else:
            raise QTArgumentError("Expected list")

    def urls(self, list_of_urs: list):
        """Create a list of existing files"""
        if isinstance(list_of_urs, list):
            self.d['urls'] = list_of_urs
        else:
            raise QTArgumentError("Expected list")

    def dictionaries(self, list_of_dictionaries: list):
        """Create a list of existing dictionary"""
        if isinstance(list_of_dictionaries, list):
            self.d['dictionaries'] = list_of_dictionaries
        else:
            raise QTArgumentError("Expected list")

    def delete(self, tag_id: str) -> bool:
        """Delete data container"""
        try:
            res = self.s.delete(self.url+tag_id, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise e
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.ok

    def search(self, string: str):
        """Search full-text and faceted search"""
        try:
            res = self.s.get(self.url+string, headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise e
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.json()

    def upload(self, file: str):
        """Upload files for data mining"""
        extension = os.path.splitext(file)[1].lower()
        try:
            if extension not in ["pdf", "txt", "html"]:
                raise QTFileTypeError("File Type Error. Allowed PDF, TXT and HTML files")
            if not os.path.exists(file):
                raise QTFileTypeError("File Not Exist. Please check your path")
            files = {'file': open(file, 'rb')}
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
            self.headers['content-type'] = 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
            res = self.s.post(self.url+"file", headers=self.headers, files=files)
        except requests.exceptions.RequestException as e:
            raise e
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.json()

    def tagging_files(self) -> bool:
        """Mine data via dictionaries"""
        if len(self.d['files']) == 0:
            raise QTDictionaryError("You must add files. Use files function to add new file in list of files")
        if len(self.d['dictionaries']) == 0:
            raise QTDictionaryError("You must add dictionaries. Use dictionaries function to add new dictionary in list of dictionaries")
        data = {'title': self.d['title'], 'files': self.d['files'], 'dictionaries': self.d['dictionaries']}
        try:
            res = self.s.post(self.url+"new", data=json.dumps(data))
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.ok

    def minning_url(self):
        """Minning data on URLs"""
        data = {'title': self.d['title'], 'urls': self.d['urls']}
        try:
            res = self.s.post(self.url + "new", data=json.dumps(data))
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error "
                                 f"{res.status_code}")
        return res.ok

    def progress(self):
        """Show progress for submitted data minining job"""
        try:
            status = self.s.get(self.url + "progress", headers=self.headers)
        except requests.exceptions.RequestException as e:
            raise QTConnectionError(f"Connection error: {e}")
        if status.status_code not in [200, 201]:
            raise QTRestApiError(f"Error: Full authentification is required to access this resource. HTTP Error"
                                 f"{status.status_code}")
        return status.json()

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
