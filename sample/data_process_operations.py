import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from qtcurate.extractor import Extractor, Mode
from qtcurate.vocabulary import Vocabulary
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt
from qtcurate.document import Document
from qtcurate.result import Result
from qtcurate.extractor import DataType
from qtcurate.field import Field, FieldValues


API_KEY = "YOUR-API-KEY"
API_KEY = "a5334f7d-2aac-44b3-aefc-a25cd9dd7bec"
DOCUMENT = "resources/sample.pdf"

# Initialise with api key
Qt.init(API_KEY, "test")

# 1- Upload the sample document for processing
list_of_documents = []
document = Document()
doc = document.create(DOCUMENT)
list_of_documents.append(doc)

# 2- Create vocabulary
vocabulary = Vocabulary()
vocabulary.add_entry("Industrials")
vocabulary.add_entry("Quasi-Governments")
vocabulary.add_entry("Governments")
vocabulary.name("Allocations (%)").create()

# 3- Creater Extractor - Regex must have 1 capturing group
extractor = Extractor()
extractor.set_vocabulary(vocabulary.get_id())
extractor.set_validator("^ +(\\d[\\d\\.\\,]+\\d)")
extractor.set_data_type(DataType.DOUBLE)

# 4- Run
dp = DataProcess()
dp.set_description("test data process")
dp.add_extractor(extractor)
dp.with_documents(list_of_documents)
dp.create()

# 5- Wait to finish
dp.wait_for_completion()

# 6- Export Field results
result = Result(dp.get_id())
for i in result.read():
    field = Field(i)
    if field.get_values() != "":
        field_value = FieldValues(field.get_values())
        print(f"{field.get_id()} {field_value.get_str()[0]}")

# 7- Export raw results to XLSX
result.result_xlsx_exporter("sample.xlsx")

# 8- Clean up
vocabulary.delete(vocabulary.get_id())
dp.delete(dp.get_id())
