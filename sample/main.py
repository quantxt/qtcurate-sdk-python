from qtcurate.dataprocess import DataProcess, DictionaryType
from qtcurate.vocabulary import Vocabulary
from qtcurate.qt import Qt
from typing import List

API_KEY = 'YOUR-API-KEY'


def get_links() -> List:
    unique_links = set()
    with open("resources/links.txt") as f:
        for line in f:
            unique_links.add(line.rstrip())
    return list(unique_links)


Qt.init(API_KEY)

voc = Vocabulary()

t = DataProcess("test")
t.title("Test Large SDK with URLS")

voc.name("loss")
voc.source("resources/loss.tsv")
try:
    voc_loss = voc.create()
except Exception as e:
    print(e)
t.search_rule(voc_loss.id, DictionaryType.NUMBER)
voc.clear()

voc.name("revenue")
voc.source("resources/revenue.tsv")
try:
    voc.create()
except Exception as e:
    print(e)

t.search_rule(voc.get_id(), DictionaryType.NUMBER)
t.urls(get_links())
t.create()
t.wait_for_completion()
t.report_to_json("report.json")
