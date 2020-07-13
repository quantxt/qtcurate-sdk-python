from qtcurate.qtdict import QtDict
from qtcurate.dataprocess import DataProcess


API_KEY = 'YOUR-API-KEY'


def create_phrases_table(key: str):
    qt_dict = QtDict(key, "test")
    qt_dict.name("Climate")
    qt_dict.add_entry("weather conditions", "Climate Conditions")
    qt_dict.add_entry("climate change", "Climate Change")
    qt_dict.add_entry("global warming", "Climate Change")
    qt_dict.create()
    climate_dictionary_id = qt_dict.get_id()
    qt_dict.clear()

    qt_dict.name("Disruption")
    qt_dict.add_entry("business disruption", "Business Disruptions")
    qt_dict.add_entry("competition", "Competition")
    qt_dict.create()
    disruption_dictionary_id = qt_dict.get_id()
    qt_dict.clear()

    return climate_dictionary_id, disruption_dictionary_id


# 1- Run once and use the dictionary IDs in future runs
clim_dic_id, disr_dic_id = create_phrases_table(API_KEY)

# 2- Initialize the API - Test environment
dp = DataProcess(API_KEY, "test")
          
# 3- Name the project
dp.title("Test 10-K labeling")
          
# 3- Set data feed and query
data_feeds = ["edgar_8k_full.json"]
dp.sources(data_feeds)
dp.query("1706524,1648636,1326089,1169561")

# 4- Pass data dictionaries
dic = QtDict(API_KEY, "test")
dic.fetch(clim_dic_id)
dp.search_rule(dic.get_id())
dic.fetch(disr_dic_id)
dp.search_rule(dic.get_id())

# 5- Run and block until finish
dp.create()
dp.wait_for_completion()

# 6- Export raw results
dp.report_to_json(dp.get_index(), "export.json")
