from qtcurate.qtdict import QtDict
from qtcurate.dataprocess import DataProcess, DictionaryType
from time import sleep

API_KEY = 'YOUR-API-KEY'

def wait_for_completion(index: str):
    percentage = 0
    while percentage < 100:
        result = dp.progress(index)
        percentage = result['progress']
        print(f"Search progress {percentage}%")
        if percentage < 100:
            sleep(1)
    sleep(5)


def create_phrases_table(key: str):
    qtdict = QtDict(key, "test")
    qtdict.name("Weather")
    qtdict.add_entry("Weather", "weather conditions")
    qtdict.add_entry("Weather", "climate change")
    qtdict.add_entry("Weather", "global warming")
    dictionary1 = qtdict.create()
    qtdict.clear()

    qtdict.name("Disruption")
    qtdict.add_entry("Disruption", "disruption")
    qtdict.add_entry("Disruption", "revenue declined")
    qtdict.add_entry("Disruption", "revenue increased")
    dictionary2 = qtdict.create()
    qtdict.clear()

    print(f"{dictionary1['id']} {dictionary2['id']}")

# 1- Run once and use the dictionary IDs in future runs
# create_phrases_table(API_KEY)

# 2- Initialize the API - Test enviroment
dp = DataProcess(API_KEY, "test")
          
# 3- Name the project
dp.title("Test 10-K labeling")
          
# 3- Set data feed and query
data_feeds = ["edgar_8k_full.json"]
dp.sources(data_feeds)
dp.query("2098,3197,4447,3116,4977")

# 4- Pass data dictionaries
dic = QtDict(API_KEY, "test")
dp.search_rule(dic.fetch("c8faa596-4f36-4fa8-818c-a89324fd92a7")["key"], DictionaryType.NONE)
dp.search_rule(dic.fetch("2b4d483a-c2b4-4f1f-bf53-7a8c9a53d236")["key"], DictionaryType.NONE)

# 5- Run and block until finish
data_process = dp.create()
wait_for_completion(data_process['index'])

# 6- Export raw results
dp.report_to_json(data_process['index'], "export.json")
