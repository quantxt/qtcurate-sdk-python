from qtcurate.model import Model
from qtcurate.qt import Qt

API_KEY = "YOUR-API-KEY"

Qt.init(API_KEY)

model = Model()

model.wait_for_completion()
