import json
import requests
import time
import aiohttp
import asyncio
from read_write_delete_duplicates import readData, writeData, delete_duplicates_list
from ratelimit import limits, RateLimitException, sleep_and_retry
from api_token import api_token_var_list

set_time = time.strftime("%Y%m%d-%H%M%S")

print('Cargando match list desde data/lor-match-data/match-lists/...')
print("\n")
match_list = readData('data/lor-match-data/match-lists/master-match_list-20220212-232705.json')

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for key in api_token_var_list:
            task = asyncio.ensure_future(get_match_info(session, key, api_token_var_list.index(key)))
            tasks.append(task)

        data = await asyncio.gather(*tasks)
        writeData('data/lor-match-data/match_data-{}.json'.format(set_time), data[0])

async def get_match_info(session, keys, index):
    TWO_MINUTES = 2
    MAX_CALLS_PER_MINUTE= 1

    hundred_match_list = match_list[2119+100*index:2219+(100*index)]

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_MINUTE, period=TWO_MINUTES)
    async def get_match_info_by_id(match_id, api_key):
        api_url = 'https://{}.api.riotgames.com/lor/match/v1/matches/{}?api_key={}'.format('americas', match_id, api_key)
        async with session.get(api_url) as response:
            result = response
            if result.status == 200:
                return await result.json(encoding='utf-8')
            else:
                return result.status
    
    counter=0
    temp_list = []

    temp_list.append({'{}'.format(api_token_var_list[index]) : []})

    print('Comenzando recolección de datos...')
    print("\n")

    for match in hundred_match_list:
        counter= counter +1
        match_info = await get_match_info_by_id(match, api_token_var_list[index])
        # print(match_info["info"]["game_type"])
        # print(match_info["info"]["game_mode"])
        # if (match_info["info"]["game_type"] == "Ranked") or (match_info["info"]["game_mode"] == "SeasonalTournamentLobby"):
    
        if match_info == 429:
            return temp_list
        if match_info == 400:
            pass
        else:
            print('Guardando datos relacionados al id: {}'.format(match))
            temp_list[index][api_token_var_list[index]].append(match_info)
    
    return temp_list

asyncio.run(main())