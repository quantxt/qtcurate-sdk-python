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

# Create Vocabulary
try:
    vocabulary.name("some name").add_entry("Apple Inc.", "AAPL").create()
except Exception as e:
    print(e)

# Fetch from current object
print("Fetch vocabulary")
print(vocabulary.fetch(vocabulary.get_id()))

# Create list of vocabularies from tsv file
print("Create list of the vocabularies from TSV file")
tsv_voc = Vocabulary()
tsv_voc.name("revenue")
tsv_voc.source(FILE_NAME)
try:
    tsv_voc.create()
except Exception as e:
    print(e)
print(tsv_voc)

# Update vocabulary, name and entries are mandatory options
print("Update vocabulary")
vocabulary.add_entry("Lenovo", "Thinkpad")
vocabulary.name("updated name")
print(vocabulary.get_id())
vocabulary.update(vocabulary.get_id())
print(vocabulary)

# List all existing vocabularies
print("List all vocabularies")
print(vocabulary.read())

# Delete vocabulary
print("Is vocabulary deleted?")
print(vocabulary.delete(vocabulary.get_id()))
