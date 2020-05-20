from qtcurate.qtdict import QtDict
from qtcurate.dataprocess import DataProcess, DictionaryType
from time import sleep

API_KEY = 'YOUR-API-KEY'
Climate_Dictionary_Id = '....'
Disruption_Dictionary_Id = '....'


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
    qtdict.name("Climate")
    qtdict.add_entry("weather conditions", "Climate Conditions")
    qtdict.add_entry("climate change", "Climate Change")
    qtdict.add_entry("global warming", "Climate Change")
    dictionary1 = qtdict.create()
    qtdict.clear()

    qtdict.name("Disruption")
    qtdict.add_entry("business disruption", "Business Disruptions")
    qtdict.add_entry("competition", "Competition")
    dictionary2 = qtdict.create()
    qtdict.clear()

    Climate_Dictionary_Id = dictionary1['id']
    Disruption_Dictionary_Id = dictionary2['id']
 #   print(f"{dictionary1['id']} {dictionary2['id']}")

# 1- Run once and use the dictionary IDs in future runs
# create_phrases_table(API_KEY)

# 2- Initialize the API - Test enviroment
dp = DataProcess(API_KEY, "test")
          
# 3- Name the project
dp.title("Test 10-K labeling")
          
# 3- Set data feed and query
data_feeds = ["edgar_8k_full.json"]
dp.sources(data_feeds)
dp.query("1706524,1648636,1326089,1169561")

# 4- Pass data dictionaries
dic = QtDict(API_KEY, "test")
dp.search_rule(dic.fetch(Climate_Dictionary_Id)["key"], DictionaryType.NONE)
dp.search_rule(dic.fetch(Disruption_Dictionary_Id)["key"], DictionaryType.NONE)

# 5- Run and block until finish
data_process = dp.create()
wait_for_completion(data_process['index'])

# 6- Export raw results
dp.report_to_json(data_process['index'], "export.json")
