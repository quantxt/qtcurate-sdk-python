import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from qtcurate.vocabulary import Vocabulary
from qtcurate.qt import Qt


API_KEY = "YOUR-API-KEY"
API_KEY = "a5334f7d-2aac-44b3-aefc-a25cd9dd7bec"

FILE_NAME = "resources/revenue.tsv"

# Initialise with api key
Qt.init(API_KEY, "test")

vocabulary = Vocabulary()
# Set name of the Vocabulary
# Create entries of vocabulary
vocabulary.add_entry("Apple Inc.", "AAPL")
vocabulary.add_entry("Amazon.com", "AMZN")
vocabulary.entries({"str": "Alphabet Inc.", "category": "GOOG"})

entry_voc = None
tsv_voc = None
# Create Vocabulary
try:
    entry_voc = vocabulary.name("some name").add_entry("Apple Inc.", "AAPL").create()
except Exception as e:
    print(e)
print(entry_voc)

# Fetch from current object
print(vocabulary.fetch(vocabulary.get_id()))
vocabulary.clear()

# Create list of dictionaries from tsv file
# Name the project
vocabulary.name("revenue")
vocabulary.source(FILE_NAME)
# Create QtDict
try:
    tsv_voc = vocabulary.create()
except Exception as e:
    print(e)
print(tsv_voc)

# Fetch from known dictionary
print(vocabulary.fetch(entry_voc.id))

# Update vocabulary, name and entries are mandatory options
new_dic = Vocabulary()
new_dic.add_entry("Lenovo", "Thinkpad")
new_dic.name("updated name")
res = new_dic.update(entry_voc.id)
print(res.id)

# List all existing dictionaries
print(vocabulary.read())
print(vocabulary.delete(entry_voc.id))
print(entry_voc)
