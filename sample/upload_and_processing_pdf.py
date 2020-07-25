from qtcurate.qtdict import QtDict
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt
from qtcurate.data_types import ChunkMode

API_KEY = "YOUR-API-KEY"
PDF = "resources/upload_sample.pdf"

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
dp.files([dp.get_uuid()])
# Run and block until finish
dp.create()
dp.wait_for_completion()

# Export raw results
dp.report_to_json("export_sample.json")

