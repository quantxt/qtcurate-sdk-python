from qtcurate.vocabulary import Vocabulary
from qtcurate.qt import Qt


API_KEY = "YOUR-API-KEY"

# Initialize with api key
Qt.init(API_KEY)

# Create entries of vocabulary
vocabulary = Vocabulary()
vocabulary.add_entry("Apple Inc.", "AAPL")
vocabulary.add_entry("Amazon.com", "AMZN")
vocabulary.entries({"str": "Alphabet Inc.", "category": "GOOG"})

entry_voc = None
# Create Vocabulary
try:
    entry_voc = vocabulary.name("some name").add_entry("Apple Inc.", "AAPL").create()
except Exception as e:
    print(e)
print(entry_voc)

# Fetch from current object
print(vocabulary.fetch(vocabulary.get_id()))
vocabulary.clear()

# Fetch from known vocabulary
print(vocabulary.fetch(entry_voc.id))

# Update an existing vocabulary
new_dic = Vocabulary()
new_dic.add_entry("Lenovo", "Thinkpad")
new_dic.name("updated name")
res = new_dic.update(entry_voc.id)
print(res.id)

# List all existing vocabularies
print(vocabulary.read())

# Delete an existing vocabulary
print(vocabulary.delete(entry_voc.id))
print(entry_voc)
