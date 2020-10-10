from qtcurate.vocabulary import Vocabulary
from qtcurate.qt import Qt


API_KEY = "YOUR-API-KEY"
FILE_NAME = "resources/revenue.tsv"

# Initialise with api key
Qt.init(API_KEY)

vocabulary = Vocabulary()
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
print(type(vocabulary.fetch(vocabulary.get_id())))
vocabulary.clear()
#
# # Create list of vocabulary from tsv file
# # Name the project
# vocabulary.name("revenue")
# vocabulary.source(FILE_NAME)
# # Create QtDict
# try:
#     tsv_voc = vocabulary.create()
# except Exception as e:
#     print(e)
# print(tsv_voc)
# # Fetch from known vocabulary
# print(vocabulary.fetch(entry_voc.id))
#
# # Update vocabulary, name and entries are mandatory options
# new_dic = Vocabulary()
# new_dic.add_entry("Lenovo", "Thinkpad")
# new_dic.name("updated name")
# res = new_dic.update(entry_voc.id)
# print(res.id)
#
# # List all existing vocabularies
# print(vocabulary.read())
# # Delete vocabulary
# print(vocabulary.delete(entry_voc.id))
