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


# create_phrases_table(API_KEY)

data_feeds = ["edgar_8k_full.json"]
dp = DataProcess(API_KEY, "test")
dp.title("Milojko test 10-K job")
dic = QtDict(API_KEY, "test")
dp.sources(data_feeds)
dp.query("1800,1961,2098,2178,2186,2488,3116,3197,3453,3499,3570,4281,4447,4962,4969,4977")
dp.search_rule(dic.fetch("c8faa596-4f36-4fa8-818c-a89324fd92a7")["key"], DictionaryType.NONE)
dp.search_rule(dic.fetch("2b4d483a-c2b4-4f1f-bf53-7a8c9a53d236")["key"], DictionaryType.NONE)

data_process = dp.create()
wait_for_completion(data_process['index'])
dp.report_to_json(data_process['index'], "export.json")