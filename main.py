from qt.tagging import Tagging, DictionaryType
from qt.dictionaries import Dictionary
from typing import List
from time import sleep


API_KEY = '1234567'


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


def wait_for_completion(index: str):
    percentage = 0
    while percentage < 100:
        result = t.progress(index)
        percentage = result['progress']
        print(f"Search progress {percentage}%")
        if percentage < 100:
            sleep(1)
    sleep(5)


d = Dictionary(api_key=API_KEY)

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
t = Tagging(api_key=API_KEY)
t.title("Test Large SDK with URLS")
t.exclude_utt_without_entities(False)
t.autotag(False)
t.search_rule(loss_dictionary['key'], DictionaryType.NUMBER)
t.search_rule(revenue_dictionary['key'], DictionaryType.NUMBER)
t.search_rule(usstocks_dictionary['key'], DictionaryType.STRING)
t.urls(get_links())
try:
    url_process = t.minning_url()
except Exception as e:
    print(e)
wait_for_completion(url_process['index'])
try:
    t.report_to_json(url_process['index'], "report.json")
except Exception as e:
    print(e)
