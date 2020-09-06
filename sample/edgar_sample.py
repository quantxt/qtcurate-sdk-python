from qtcurate.vocabulary import Vocabulary
from qtcurate.dataprocess import DataProcess
from qtcurate.qt import Qt
from qtcurate.data_types import ChunkMode

API_KEY = 'YOUR-API-KEY'


def create_phrases_table():
    voc = Vocabulary("test")
    voc.name("Climate")
    voc.add_entry("weather conditions", "Climate Conditions")
    voc.add_entry("climate change", "Climate Change")
    voc.add_entry("global warming", "Climate Change")
    climate_dictionary = voc.create()
    voc.clear()

    voc.name("Disruption")
    voc.add_entry("business disruption", "Business Disruptions")
    voc.add_entry("competition", "Competition")
    disruption_dictionary = voc.create()
    voc.clear()

    return climate_dictionary.id, disruption_dictionary.id


Qt.init(API_KEY)

# 1- Run once and use the dictionary IDs in future runs
clim_dic_id, disr_dic_id = create_phrases_table()

# 2- Initialize the API - Test environment
dp = DataProcess("test")
          
# 3- Name the project
dp.title("Transcript labeling test")

# 4- Set numWorkers
dp.set_workers(32)

# 5- Set data feed and query
data_feeds = ["edgar_8k_full.json"]
dp.set_chunk(ChunkMode.SENTENCE)
dp.sources(data_feeds)
dp.query("1706524,1648636,1326089,1169561")

# 6- Pass data dictionaries, two ways, directly from object and from response
voc = Vocabulary("test")
dic1 = voc.fetch(clim_dic_id)
dp.search_rule(dic1.id)
voc.fetch(disr_dic_id)
dp.search_rule(voc.get_id())

# 7- Run and block until finish
dp.create()
dp.wait_for_completion()

# 8- Export raw results
dp.report_to_json("export.json")
