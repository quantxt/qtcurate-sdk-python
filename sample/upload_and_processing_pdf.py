import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from qtcurate.qtdict import QtDict
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt
from qtcurate.data_types import ChunkMode

API_KEY = "YOUR-API-KEY"
API_KEY = "a5334f7d-2aac-44b3-aefc-a25cd9dd7bec"

PDF = "resources/upload_sample.pdf"

list_of_files = []
# Initialise with api key
Qt.init(API_KEY)
dic = QtDict()
dic.name("Regular expressions")
# Create entries of dictionaries
dic.add_entry("Regular expressions", "Regular expressions")
# Create QtDict
dic.create()

dp = DataProcess()
# Name the project
dp.title("testPdf")
# Add dictionary id
dp.search_rule(dic.get_id())
# Set parameter for splitting documents
dp.set_chunk(ChunkMode.PAGE)
# Upload file for processing
dp.upload(PDF)
list_of_files.append(dp.get_uuid())
dp.files(list_of_files)
# Run and block until finish
dp.create()
dp.wait_for_completion()

# Export raw results to JSON
dp.report_to_json("export_sample.json")

# Export raw results to XLSX
dp.report_to_xlsx("export_sample.xlsx")

