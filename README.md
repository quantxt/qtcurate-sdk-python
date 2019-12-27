# qtcurate-sdk-python
Python SKD for Search and Data extraction
## Installation

```
pip install name-of-package
```

## USAGE

How to use

### Data Dictionaries

Authentication with API KEY
```
d = Dictionary(api_key='1234567')
```

List Available Dictionaries
```
try:
    all_dict = d.list()
except Exception as e:
    print(e)
print(all_dict)
```

Fetch existing dictionary
```
dict_id = "c6cf04a6-f5a7-45f7-943c-7e961d37f2bf"
try:
    one_dict = d.fetch(dict_id)
except Exception as e:
    print(e)
print(one_dict)
```

To delete existing dictionary
```
try:
    d.delete(dict_id)
except Exception as e:
    print(e)
```

Create new dictionary
```
dict1 = {'key': 1}
dict2 = {'key': 1, "value": 3}
d.name('Name of dictionary')
```
Adding one pair key-value
```
d.add_entry("key1", "value1")
```
Adding dictionary or multiple dictionary
```
d.entries(dict1)
d.entries(dict2)

try:
    a = d.create()
except Exception as e:
    print(e)
```

Update existing dictionary
```
dict_id = "klakljhas23asf"
try:
    a = d.update(dict_id)
except Exception as e:
    print(e)
```

Delete existing dictionary
```
try:
    d.delete(dict_id)
except Exception as e:
    print(e)
```

Create dictionary from TSV files
```
try:
    d.upload("sample.tsv")
except Exception as e:
    print(e)
```

### Extraction and Mining
Authentication with API KEY
```
t = Tagging(api_key='1234567')
```

First, upload all content files for tagging via the following function. PDF, TXT and HTML formats are supported.
```
file_name = "file.pdf"
try:
    t.upload(file_name)
except Exception as e:
    print(e)
```
Then you can mine data via dictionaries
```
list_of_files = ["file1", "file2"]
list_of_dictionaries = ["dict1","dict2"]
d.title("some title")
d.files(list_of_files)
d.dictionaries(list_of_dictionaries)
try:
    t.tagging_files(file_name)
except Exception as e:
    print(e)
```
To delete a data container
```
try:
    t.delete(tag_id)
except Exception as e:
    print(e)
```
Mining web URLs
```
urls = ["www.google.com", "www.yahoo.com"]
d.title("title")
d.urls(urls)

try:
    t.mining_url()
except Exception as e:
    print(e)
```
Status monitoring
```
try:
    t.progress()
except Exception as e:
    print(e)
```
Full text and faceted search in the extracted data
```
element = "element"
try:
    t.search(something)
except Exception as e:
    print(e)
```
### Exporting the Results
Exporting in Excel Format
```
element = "element"
path = "name of new xlsx file with full path"
try:
    t.report_to_xslx(element, path)
except Exception as e:
    print(e)
```

Exporting in JSON Format
```
element = "element"
path = "name of new json file with full path"
try:
    t.report_to_xslx(element, path)
except Exception as e:
    print(e)
```