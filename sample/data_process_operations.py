from qtcurate.extractor import Extractor, Type
from qtcurate.vocabulary import Vocabulary
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt
from qtcurate.document import Document
from qtcurate.result import Result
from qtcurate.result import Field, FieldValue


API_KEY = "YOUR-API-KEY"
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
vocabulary.set_vocab_name("Allocations (%)").create()

# 3- Creator Extractor - Regex must have 1 capturing group
extractor = Extractor()
extractor.set_vocabulary(vocabulary.get_id())
extractor.set_validator("^ +(\\d[\\d\\.\\,]+\\d)")
extractor.set_type(Type.DOUBLE)

# 4- Run
dataprocess = DataProcess()
dataprocess.set_description("test data process")
dataprocess.add_extractor(extractor)
dataprocess.with_documents(list_of_documents)
dataprocess.create()

# 5- Wait to finish
dataprocess.wait_for_completion()

# 6- Export Field results
result = Result(dataprocess.get_id())
# print(result.read())
for item in result.read():
    field_value = item.get_values()[0]
    print(f"{item.get_str()} -> {field_value.get_str()}")

# 7- Export raw results to XLSX
result.result_xlsx_exporter("sample.xlsx")

# 8- Clean up
vocabulary.delete(vocabulary.get_id())
dataprocess.delete(dataprocess.get_id())
