from qtcurate.qt import Qt
from qtcurate.dataprocess import DataProcess


API_KEY = "YOUR_API_KEY"
file_name = "report.xlsx"

Qt.init(API_KEY)

some_dataprocessor_id = "khbqokqyvk"
dp = DataProcess()
dp.set_id(some_dataprocessor_id)
dp.report_to_xlsx(file_name)
