from qtcurate.qt import Qt
from qtcurate.result import Result


API_KEY = "YOUR-API-KEY"

Qt.init(API_KEY)

model_id = "__jobid__"

result = Result(model_id)

result.result_xlsx_exporter("name of file example export.xlsx")

result.raw_exporter("name of JSON file example export.json")
