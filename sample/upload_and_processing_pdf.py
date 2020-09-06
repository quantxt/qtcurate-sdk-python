from qtcurate.vocabulary import Vocabulary
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt
from qtcurate.data_types import ChunkMode

API_KEY = "YOUR-API-KEY"

PDF = "resources/upload_sample.pdf"

list_of_files = []
# Initialise with api key
Qt.init(API_KEY)
voc = Vocabulary()
voc.name("Regular expressions")
# Create entries of dictionaries
voc.add_entry("Regular expressions", "Regular expressions")
# Create QtDict
voc.create()

dp = DataProcess()
# Name the project
dp.title("testPdf")
# Add dictionary id
dp.search_rule(voc.get_id())
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

