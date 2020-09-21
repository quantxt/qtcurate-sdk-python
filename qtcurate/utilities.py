from qtcurate.exceptions import QtConnectionError, QtRestApiError, QtArgumentError
import requests
from typing import Dict, Tuple
import json
from collections import namedtuple


def json_to_tuple(data: [str, Dict]) -> Tuple:
    if "global" in data.keys():
        data["Global"] = data.pop("global")
    if isinstance(data, Dict):
        data = json.dumps(data)
    if not isinstance(data, str):
        raise QtArgumentError("This is not valid type of object")

    return json.loads(data, object_hook=lambda d: namedtuple('Object', d.keys())(*d.values()))


def connect(method: str, uri: str, headers: str, data_type: str = None, data=None) -> Dict:
    if data_type not in [None, "data", "files", "params"]:
        raise QtArgumentError("Unknown data type. params, data and files are allowed")
    if method.lower() == 'get':
        if data_type is None:
            try:
                res = requests.get(uri, headers=headers)
            except requests.exceptions.RequestException as e:
                raise QtConnectionError(f"Connection error: {e}")
            if res.status_code not in [200, 201, 202, 204]:
                raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                     f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        elif data_type == "params":
            try:
                res = requests.get(uri, headers=headers, params=data)
            except requests.exceptions.RequestException as e:
                raise QtConnectionError(f"Connection error: {e}")
            if res.status_code not in [200, 201, 202, 204]:
                raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                     f"HTTP status code: {res.status_code}. Server message: {res.json()}")
    elif method.lower() == "delete":
        try:
            res = requests.delete(uri, headers=headers)
        except requests.exceptions.RequestException as e:
            raise QtConnectionError(f"Connection error: {e}")
        if res.status_code not in [200, 201, 202, 204]:
            raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                 f"HTTP status code: {res.status_code}. Server message: {res.json()}")
    elif method.lower() == "post":
        if data_type == "data":
            try:
                res = requests.post(uri, headers=headers, data=data)
            except requests.exceptions.RequestException as e:
                raise QtConnectionError(f"Connection error: {e}")
            if res.status_code not in [200, 201, 202, 204]:
                raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                     f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        elif data_type == "files":
            try:
                res = requests.post(uri, headers=headers, files=data)
            except requests.exceptions.RequestException as e:
                raise QtConnectionError(f"Connection error: {e}")
            if res.status_code not in [200, 201, 202, 204]:
                raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                     f"HTTP status code: {res.status_code}. Server message: {res.json()}")

    elif method.lower() == "put":
        if data_type == "data":
            try:
                res = requests.put(uri, headers=headers, data=data)
            except requests.exceptions.RequestException as e:
                raise QtConnectionError(f"Connection error: {e}")
            if res.status_code not in [200, 201, 202, 204]:
                raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                     f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        elif data_type == "files":
            try:
                res = requests.put(uri, headers=headers, files=data)
            except requests.exceptions.RequestException as e:
                raise QtConnectionError(f"Connection error: {e}")
            if res.status_code not in [200, 201, 202, 204]:
                raise QtRestApiError(f"HTTP error: Full authentication is required to access this resource. "
                                     f"HTTP status code: {res.status_code}. Server message: {res.json()}")
        else:
            raise QtArgumentError("Unknown data type. data and files are allowed")
    return res
