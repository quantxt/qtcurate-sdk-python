# import sys
# import os
#
# sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from qtcurate.dataprocess import DataProcess, DictionaryType
from qtcurate.qtdict import QtDict
from qtcurate.utilities import wait_for_completion
from typing import List


API_KEY = 'YOUR-API-KEY'


def get_dictionary_entries(file_name: str) -> List:
    entries = []
    with open(file_name) as f:
        for line in f:
            temp_dict = dict()
            (key, value) = line.split("\t")
            temp_dict['key'] = key.rstrip()
            temp_dict['value'] = value.rstrip()
            entries.append(temp_dict)
    return entries


def get_links() -> List:
    unique_links = set()
    with open("links.txt") as f:
        for line in f:
            unique_links.add(line.rstrip())
    return list(unique_links)



d = QtDict(API_KEY, "test")

loss_entries = get_dictionary_entries("loss.tsv")
revenue_entries = get_dictionary_entries("revenue.tsv")
usstocks_entries = get_dictionary_entries("usstocks.tsv")

d.name("loss")
for entry in loss_entries:
    d.entries(entry)
try:
    loss_dictionary = d.create()
except Exception as e:
    print(e)

d.clear()

d.name("revenue")
for entry in revenue_entries:
    d.entries(entry)

try:
    revenue_dictionary = d.create()

except Exception as e:
    print(e)

d.clear()

d.name("usstocks")
for entry in usstocks_entries:
    d.entries(entry)
try:
    usstocks_dictionary = d.create()
except Exception as e:
    print(e)
print(loss_dictionary['key'])
t = DataProcess(API_KEY, "test")
t.title("Test Large SDK with URLS")
t.exclude_utt_without_entities(False)
t.autotag(False)
t.search_rule(loss_dictionary['key'], DictionaryType.NUMBER)
t.search_rule(revenue_dictionary['key'], DictionaryType.NUMBER)
t.search_rule(usstocks_dictionary['key'], DictionaryType.STRING)
t.urls(get_links())
url_process = t.create()
wait_for_completion(url_process['index'], t)
t.report_to_json(url_process['index'], "report.json")
