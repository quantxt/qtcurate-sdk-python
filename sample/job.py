from qtcurate.qt import Qt
from qtcurate.result import Result

API_KEY = "YOUR_API_KEY"
DOCUMENT = "resources/Bahia.xls"
MODEL_ID = "cigkzgmxhp"
Qt.init(API_KEY)

result = Result(MODEL_ID)
for item in result.read():
    field_value = item.get_values()
    if field_value:
        for val in field_value:
            print(f"{val.get_position().get_start()} -> {val.get_position().get_end()} -> {val.get_position().get_line()}")
