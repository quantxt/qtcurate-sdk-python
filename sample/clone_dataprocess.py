# To clone a project and process fresh data. We continue upload_and_processing_pdf.py
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt
from qtcurate.data_types import ChunkMode

API_KEY = "YOUR-API-KEY"
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
