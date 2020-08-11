from qtcurate.qtdict import QtDict
from qtcurate.qt import Qt
from typing import List


API_KEY = "YOUR-API-KEY"
FILE_NAME = "resources/revenue.tsv"


# Function for creating list of dictionaries from tsv file
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


# Initialise with api key
Qt.init(API_KEY)

dic = QtDict()
# Set name of the QtDict
dic.name("some_name")
# Create entries of dictionaries
dic.add_entry("Apple Inc.", "AAPL")
dic.add_entry("Amazon.com", "AMZN")
dic.entries({"str": "Alphabet Inc.", "category": "GOOG"})

entry_dic = None
# Create QtDict
try:
    entry_dic = dic.create()
except Exception as e:
    print(e)

dic.clear()

# Create list of dictionaries from tsv file
revenue_entries = get_dictionary_entries(FILE_NAME)
# Name the project
dic.name("revenue")
# Create entries of dictionaries
for entry in revenue_entries:
    dic.entries(entry)

# Create QtDict
try:
    dic.create()
except Exception as e:
    print(e)

# Fetch from current object
print(dic.fetch(dic.get_id()))

# Fetch from known dictionary
print(dic.fetch(entry_dic.id))

# Update dictionary, name and entries are mandatory options
new_dic = QtDict()
new_dic.add_entry("mima", "masha")
new_dic.name("updated name")
res = new_dic.update(entry_dic.id)
print(res.id)

# List all existing dictionaries
print(dic.list())
print(dic.delete(entry_dic.id))

print(entry_dic)