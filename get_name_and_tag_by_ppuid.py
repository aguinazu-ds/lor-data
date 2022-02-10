import json
import requests
from api_token import api_token_var

def get_name_and_tag_by_ppuid(region, ppuid):
    """"""
    api_url_base = 'https://{}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}?api_key={}'
    api_url = api_url_base.format(region, ppuid, api_token_var)

    respuesta = requests.get(api_url)

    if respuesta.status_code == 200:
        return json.loads(respuesta.content.decode('utf-8'))
    else:
        return print(respuesta.status_code)