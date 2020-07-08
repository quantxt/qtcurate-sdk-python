from qtcurate.qtdict import QtDict
from typing import List

API_KEY = 'YOUR-API-KEY'
FILE_NAME = "revenue.tsv"


def get_dictionary_entries(file_name: str) -> List:
    entries = []
    with open(file_name) as f:
        for line in f:
            temp_dict = dict()
            (key, value) = line.split("\t")
            temp_dict['str'] = key.rstrip()
            temp_dict['category'] = value.rstrip()
            entries.append(temp_dict)
    return entries


dic = QtDict(API_KEY)
dic.name("some_name")
dic.add_entry("Apple Inc.", "AAPL")
dic.add_entry("Amazon.com", "AMZN")
dic.entries({"str": "Alphabet Inc.", "category": "GOOG"})
try:
    entry_dic = dic.create()
except Exception as e:
    print(e)
dic.clear()

dic = QtDict(API_KEY)
revenue_entries = get_dictionary_entries("revenue.tsv")
dic.name("revenue")
for entry in revenue_entries:
    dic.entries(entry)
try:
    revenue_dic = dic.create()
except Exception as e:
    print(e)
