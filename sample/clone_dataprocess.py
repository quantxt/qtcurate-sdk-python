# To clone a project and process fresh data. We continue upload_and_processing_pdf.py
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt
from qtcurate.data_types import ChunkMode

API_KEY = "YOUR-API-KEY"
API_KEY = "a5334f7d-2aac-44b3-aefc-a25cd9dd7bec"

additional_file = "resources/new_pdf.pdf"
some_dataprocessor_id = "khbqokqyvk"
list_of_files = []
Qt.init(API_KEY)
dp = DataProcess()
dp.title("clone dataprocess")
dp.set_chunk(ChunkMode.PAGE)
dp.upload(additional_file)
list_of_files.append(dp.get_uuid())
dp.files(list_of_files)
dp.clone(some_dataprocessor_id)
print(dp.get_id())
