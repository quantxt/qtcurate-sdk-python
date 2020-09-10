from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt

API_KEY = "YOUR-API-KEY"

Qt.init(API_KEY)

dp = DataProcess()

dp.wait_for_completion()
