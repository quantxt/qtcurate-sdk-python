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
DOCUMENT = "resources/sample.pdf"

# Initialize with api key
Qt.init(API_KEY)

# 1- Upload the sample document for processing
list_of_documents = []
document = Document()
doc = document.create(DOCUMENT)
list_of_documents.append(doc)

# 2- Create vocabulary
voc = Vocabulary()
voc.add_entry("Industrials")
voc.add_entry("Quasi-Governments")
voc.add_entry("Governments")
voc.name("Allocations (%)").create()

# 3- Create Extractor - Regex must have 1 capturing group
extractor = Extractor()
extractor.set_vocabulary(voc.get_id())
extractor.set_validator("^ +(\\d[\\d\\.\\,]+\\d)")
extractor.set_data_type(DataType.DOUBLE)

# 4- Run
dp = DataProcess()
dp.title("My parser job")
dp.with_extractor(extractor)
dp.withDocuments(list_of_documents)
dp.create()

# 5- Wait to finish
dp.wait_for_completion()

# 6- Export Field results
result = Result(dp.get_id())
for i in result.read():
    field = Field(i)
    print(f"{field.get_search_id()} {field.get_title()}")
    
# 7- Export raw results to XLSX
result.result_xlsx_exporter("sample.xlsx")

# 8- Clean up
voc.delete(voc.get_id())
dp.delete(dp.get_id())
