import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from qtcurate.extractor import Extractor
from qtcurate.vocabulary import Vocabulary
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt
from qtcurate.document import Document
from qtcurate.result import Result
from qtcurate.extractor import DataType
from qtcurate.field import Field


API_KEY = "YOUR-API-KEY"
SEARCH_PDF = "resources/sample.pdf"

list_of_files = []
# Initialise with api key
Qt.init(API_KEY)
voc = Vocabulary()
voc.name("Regular expressions")
# Create entries of dictionaries
voc.add_entry("Industrials")
voc.add_entry("Quasi-Governments")
voc.add_entry("Governments")
# Create QtDict
voc.name("Allocations (%)").create()

document = Document()
doc = document.create(SEARCH_PDF)
list_of_files.append(doc)

extractor = Extractor()
extractor.set_vocabulary(voc.get_id())
extractor.set_validator("^ +(\\d[\\d\\.\\,]+\\d)")
extractor.set_data_type(DataType.DOUBLE)

dp = DataProcess()
# Name the project
dp.title("testPdf")

dp.with_extractor(extractor)
dp.withDocuments(list_of_files)
# Run and block until finish
dp.create()
dp.wait_for_completion()

result = Result(dp.get_id())

# Export raw results to XLSX
result.result_xlsx_exporter("sample.xlsx")

for i in result.read():
    field = Field(i)
    print(f"{field.get_search_id()} {field.get_title()}")

voc.delete(voc.get_id())
dp.delete(dp.get_id())
