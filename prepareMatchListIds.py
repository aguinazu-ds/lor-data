from read_write_delete_duplicates import readData, writeData, delete_duplicates_list
import time
from api_token import api_token_var_list

set_time = time.strftime("%Y%m%d-%H%M%S")

old_match_list = readData('data/lor-match-data/match-lists/master-match_list-20220212-232705.json')
new_match_list = readData('data/lor-match-data/match-lists/master-match-list-20220215-173708.json')

temp_list = []

for match in new_match_list:
    if match not in old_match_list:
        temp_list.append(match)

temp_list = delete_duplicates_list(temp_list)

subset_count = int(len(temp_list)/(100*len(api_token_var_list))) + 1

subset_list = [temp_list[x:(x+100*len(api_token_var_list))] for x in range(0, len(temp_list), 100*len(api_token_var_list))]

for set in subset_list:
    writeData('data/lor-match-data/match-lists/masterMatchList(p{})-{}.json'.format(subset_list.index(set),set_time), set)