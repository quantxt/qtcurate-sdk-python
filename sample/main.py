from qtcurate.dataprocess import DataProcess, DictionaryType
from qtcurate.qtdict import QtDict
from typing import List

API_KEY = 'YOUR-API-KEY'


def get_dictionary_entries(file_name: str) -> List:
    entries = []
    with open(file_name) as f:
        for line in f:
            temp_dict = dict()
            (category, str_value) = line.split("\t")
            temp_dict['category'] = category.rstrip()
            temp_dict['str'] = str_value.rstrip()
            entries.append(temp_dict)
    return entries


def get_links() -> List:
    unique_links = set()
    with open("resources/links.txt") as f:
        for line in f:
            unique_links.add(line.rstrip())
    return list(unique_links)


d = QtDict(API_KEY, "test")

loss_entries = get_dictionary_entries("resources/loss.tsv")
revenue_entries = get_dictionary_entries("resources/revenue.tsv")

t = DataProcess(API_KEY, "test")
t.title("Test Large SDK with URLS")

d.name("loss")
for entry in loss_entries:
    d.entries(entry)
try:
    d.create()
except Exception as e:
    print(e)
t.search_rule(d.get_id(), DictionaryType.NUMBER)
d.clear()

d.name("revenue")
for entry in revenue_entries:
    d.entries(entry)

try:
    d.create()

except Exception as e:
    print(e)

t.search_rule(d.get_id(), DictionaryType.NUMBER)
t.urls(get_links())
t.create()
t.wait_for_completion()
t.report_to_json(t.get_index(), "report.json")
