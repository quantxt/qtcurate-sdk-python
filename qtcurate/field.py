from typing import List

class Field:
    def __init__(self, result: List):
        self.search_id = result["searchId"]
        if "title" in result:
            self.title = result["title"]
        else:
            self.title = ""
        if "id" in result:
            self.id = result["id"]
        else:
            self.id = ""
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
        if "language" in result:
            self.language = result["language"]
        else:
            self.language = ""
        if "position" in result:
            self.position = result["position"]
        else:
            self.position = ""
        if "values" in result:
            self.values = result["values"]
        else:
            self.values = ""

    def get_search_id(self):
        return self.search_id

    def get_title(self):
        return self.title

    def get_id(self):
        if self.id is not None:
            return self.id
        return None

    def get_source(self):
        return self.source

    def get_link(self):
        return self.source

    def get_date(self):
        return self.date

    def get_language(self):
        return self.language

    def get_position(self):
        return self.position

    def get_values(self):
        return self.values


