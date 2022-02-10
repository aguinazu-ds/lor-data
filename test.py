import json
import requests
from api_token import api_token_var
from add_entry import add_entry
from write_to_json import write_to_json
from get_match_info_by_id import get_match_info_by_id
from get_matchs_by_ppuid import get_matchs_by_ppuid
from get_name_and_tag_by_ppuid import get_name_and_tag_by_ppuid
from get_player_puuid import get_player_puuid

regions = ['americas', 'europe', 'sea']
ppuid = 'PfzClN0fv3aqfVPwfqiIV-lZNPIjmIpPyInqBiTvfsbvb0LMXhlrQCamZiGg7ib9twYINcsbMz6Hxg' #Aikado master player verificado

list_of_matches = get_matchs_by_ppuid(ppuid, regions[0])

match_info = get_match_info_by_id(regions[0], list_of_matches[0])

try:
    with open ('data/lor-player-data/match_data.json', mode="r+") as file:
        file.seek(0,2)
        position = file.tell() -1
        file.seek(position)
        file.write( ",{}]".format(json.dumps(match_info, ensure_ascii=False, indent=4)))
    # with open("data/lor-player-data/match_data.json", "r+") as file:
    #     data = json.load(file)
    #     data.update(match_info)
    #     file.seek(0)
    #     json.dump(data, file, ensure_ascii=False, indent=4)
except:
    with open('data/lor-player-data/match_data.json', 'w') as file:
        json.dump(match_info, file, ensure_ascii=False, indent=4)