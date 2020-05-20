# import sys
# import os
#
# sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from qtcurate.qtdict import QtDict
from qtcurate.dataprocess import DataProcess, DictionaryType
from qtcurate.utilities import wait_for_completion


API_KEY = 'YOUR-API-KEY'


def create_phrases_table(key: str):
    qt_dict = QtDict(key, "test")
    qt_dict.name("Climate")
    qt_dict.add_entry("weather conditions", "Climate Conditions")
    qt_dict.add_entry("climate change", "Climate Change")
    qt_dict.add_entry("global warming", "Climate Change")
    dictionary1 = qt_dict.create()
    qt_dict.clear()

    qt_dict.name("Disruption")
    qt_dict.add_entry("business disruption", "Business Disruptions")
    qt_dict.add_entry("competition", "Competition")
    dictionary2 = qt_dict.create()
    qt_dict.clear()

    climate_dictionary_id = dictionary1['id']
    disruption_dictionary_id = dictionary2['id']
    return climate_dictionary_id, disruption_dictionary_id


# 1- Run once and use the dictionary IDs in future runs
clim_dic_id, disr_dic_id = create_phrases_table(API_KEY)

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
dp.search_rule(dic.fetch(clim_dic_id)["key"], DictionaryType.NONE)
dp.search_rule(dic.fetch(disr_dic_id)["key"], DictionaryType.NONE)

# 5- Run and block until finish
data_process = dp.create()
wait_for_completion(data_process['index'], dp)

# 6- Export raw results
dp.report_to_json(data_process['index'], "export.json")
