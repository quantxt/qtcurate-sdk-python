# To clone a project and process fresh data. We continue upload_and_processing_pdf.py
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt

API_KEY = "YOUR-API-KEY"

additional_file = "resources/new_pdf.pdf"
some_dataprocessor_id = "YOUR-DATAPROCESS-ID"
list_of_files = []
Qt.init(API_KEY)
dp = DataProcess()
dp.title("clone dataprocess")
dp.upload(additional_file)
list_of_files.append(dp.get_uuid())
dp.files(list_of_files)

new_dp = dp.clone(some_dataprocessor_id)
# print new cloned data process
print(new_dp)

print(new_dp.id)

