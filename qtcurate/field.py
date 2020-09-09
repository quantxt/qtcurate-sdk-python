from typing import List

class Field:
    def __init__(self, result: List):
        self.search_id = result["searchId"]
        if "title" in result:
            self.title = result["title"]
        else:
            self.title = ""
        if "source" in result:
            self.source = result["source"]
        else:
            self.source = ""
        if "link" in result:
            self.link = result["link"]
        else:
            self.link = ""
        if "date" in result:
            self.date = result["date"]
        else:
            self.date = ""
        if "position" in result:
            self.position = result["position"]
        else:
            self.position = ""
        if "values" in result:
            self.values = result["values"]
        else:
            self.values = ""

    def get_id(self):
        return self.search_id

    def get_title(self):
        return self.title

    def get_source(self):
        return self.source

    def get_link(self):
        return self.source

    def get_date(self):
        return self.date

    def get_position(self):
        return self.position

    def get_values(self):
        return self.values

class FieldValues:

    def __init__(self, values: List):
        if "dict_name" in values:
            self.vocab_name = values["dict_name"]
        if "dict_id" in values:
            self.vocab_id = values["dict_id"]
        if "category" in values:
            self.category = values["category"]
        if "type" in values:
            self.type = values["type"]
        if "str" in values:
            self.str = values["str"]

