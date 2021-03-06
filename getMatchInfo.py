import time
import aiohttp
import asyncio
from read_write_delete_duplicates import readData, writeData, delete_duplicates_list
from ratelimit import limits, RateLimitException, sleep_and_retry
from api_token import api_token_var_list

# Función para transformar Lista de listas a una sola lista [[a],[b],[c]] ---> [a,b,c] 
def flatten(t):
    return [item for sublist in t for item in sublist]

# Fijamos el tiempo cuando se ejecutó el script para guardar el archivo con la info que se obtuvo, con fecha y hora.
set_time = time.strftime("%Y%m%d-%H%M%S")

print('Cargando match list desde data/lor-match-data/match-lists/...')
print("\n")
# Cargamos el archivo que contiene los match ids de los que queremos obtener información
match_list = readData('data/lor-match-data/match-lists/masterMatchList(p2)-20220215-225658.json')
# match_list = match_list_data_load[4099:]


async def main():
    async with aiohttp.ClientSession() as session:

        tasks = []

        # Iteramos por todas las API Keys que tenemos. Estas keys están guardadas en el archivo api_token.py (Son 21 keys)
        for key in api_token_var_list:
            task = asyncio.ensure_future(get_match_info(session, key, api_token_var_list.index(key)))
            tasks.append(task)

        data = await asyncio.gather(*tasks)
        writeData('data/lor-match-data/match_data-{}.json'.format(set_time), flatten(data))


# Función que queremos correr de manera asincronica, sin esperar a que cada API call termine.
async def get_match_info(session, key, index):

    #Restricción para que la función solo se llame 1 vez cada 1.5 segundos y así no pasar el limite de 100 llamadas cada 120 segundos que impone riot.
    @sleep_and_retry
    @limits(calls=1, period=1.25)
    @limits(calls=100, period=3600)
    async def get_match_info_by_id(match_id, api_key):
        api_url = 'https://{}.api.riotgames.com/lor/match/v1/matches/{}?api_key={}'.format('americas', match_id, api_key)
        async with session.get(api_url) as response:
            # result = response
            if response.status == 200:
                return await response.json(encoding='utf-8'), response
            else:
                return response.status, response
    
    # Contador paa saber en que id de la match list obtivimos algún error
    counter=0

    temp_list = []

    temp_list.append({'{}'.format(key) : []})

    for id_index in range(len(match_list)):

        if (len(api_token_var_list)*id_index + index) > len(match_list) -1:
            print('Termina API KEY {} en Paso: {}'.format(key,counter))
            return temp_list

        counter= len(api_token_var_list)*id_index + index + 1

        

        match_info = await get_match_info_by_id(match_list[len(api_token_var_list)*id_index + index], key)

        # · El error 429, es cuando pasamos alguno de los limites que impone Riot al hacer API Calls.
        # Para las API Keys que tengo yo (21 keys), cada una tiene un límite de 1 llamada cada 20seg o 100 llamadas cada 120 seg.
        # Además, cada tipo de llamada tiene su límite, en el caso de esta función, cuando llamamos a la URL de riot para obtener
        # información (linea 46 y 47), este método en particular tiene un límite de 100 llamadas cada una hora.
        # · El error 400 es cuando no se encuentra información (en los servidores de Riot) asociada a el match id solicitado.
        if match_info[0] == 429:
            print("\n")
            print('Error en paso nº{}'.format(counter))
            print('Error 429, rate limit alcanzado.')
            print('"X-App-Rate-Limit-Count": {}'.format(match_info[1].headers["X-App-Rate-Limit-Count"]))
            print('"X-Method-Rate-Limit-Count": {}'.format(match_info[1].headers["X-Method-Rate-Limit-Count"]))
            return temp_list
        elif match_info[0] == 404:
            print("\n")
            print('Error en paso nº{}'.format(counter))
            print('Error 404, no se encontro información relacionada al id {}'.format(match_list[len(api_token_var_list)*id_index + index]))
            pass
        elif match_info[0] == 403:
            print("\n")
            print('Error 403 en paso nº{}'.format(counter))
            print('Revisar vigencia API Key {}'.format(key))
        else:
            print('Guardando datos relacionados al id: {}'.format(match_list[len(api_token_var_list)*id_index + index]))
            temp_list[0][key].append(match_info[0])
    
    return temp_list


asyncio.run(main())