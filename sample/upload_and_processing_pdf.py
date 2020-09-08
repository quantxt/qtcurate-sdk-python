import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from qtcurate.vocabulary import Vocabulary
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt
from qtcurate.data_types import ChunkMode
from qtcurate.document import Document
from qtcurate.result import Result


API_KEY = "YOUR-API-KEY"
API_KEY = "a5334f7d-2aac-44b3-aefc-a25cd9dd7bec"

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

document = Document()
dp = DataProcess()
# Name the project
dp.title("testPdf")
# Add dictionary id
dp.search_rule(voc.get_id())
# Set parameter for splitting documents
dp.set_chunk(ChunkMode.PAGE)
# Upload file for processing
doc = document.create(PDF, "test create document")
list_of_files.append(doc.uuid)
dp.files(list_of_files)
# Run and block until finish
dp.create()
dp.wait_for_completion()

result = Result(dp.get_id())

# Export raw results to JSON
result.raw_exporter("export_sample.json")

# Export raw results to XLSX
result.result_xlsx_exporter("export_sample.xlsx")

