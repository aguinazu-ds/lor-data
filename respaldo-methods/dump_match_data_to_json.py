import json
import requests
import time
from api_token import api_token_var
from get_match_info_by_id import get_match_info_by_id
from get_matchs_by_ppuid import get_matchs_by_ppuid

# regions = ['americas', 'europe', 'sea']
# ppuid = 'PfzClN0fv3aqfVPwfqiIV-lZNPIjmIpPyInqBiTvfsbvb0LMXhlrQCamZiGg7ib9twYINcsbMz6Hxg' #Aikado master player verificado

# ppuid = '4xZwHkxuTzAjZRicTZsRGoEyYIlB1b0wJrfc7eBJHJU05O9n3zc_hjxbzZmRKKbysio5YxMwKrB1hA' # este ppui es de bear barmitzva master verefied.

def dump_match_data_to_json(ppuid, region):
    """"""
    list_of_matches = get_matchs_by_ppuid(ppuid, region)
    temp_list = []

    for i in range(len(list_of_matches)):
        match_info = get_match_info_by_id(region, list_of_matches[i])
        if match_info["info"]["game_mode"] == "SeasonalTournamentLobby" or match_info["info"]["game_type"] == "Ranked" :
            temp_list.append(match_info)

    with open('data/lor-match-data/match_data-{}.json'.format(time.strftime("%Y%m%d-%H%M%S")), 'w') as file:
            file.write(format(json.dumps(temp_list, ensure_ascii=False, indent=4)))