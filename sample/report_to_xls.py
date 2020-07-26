import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from qtcurate.qt import Qt
from qtcurate.dataprocess import DataProcess


API_KEY = "YOUR_API_KEY"
file_name = "report.xlsx"
API_KEY = "a5334f7d-2aac-44b3-aefc-a25cd9dd7bec"

Qt.init(API_KEY)

some_dataprocessor_id = "khbqokqyvk"
dp = DataProcess()
dp.set_id(some_dataprocessor_id)
dp.report_to_xlsx(file_name)
