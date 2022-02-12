import json
import requests
from api_token import api_token_var
from ratelimit import limits

ONE_MINUTES = 60

@limits(calls=1000, period= ONE_MINUTES)
def get_name_and_tag_by_ppuid(region, ppuid):
    """"""
    api_url = 'https://{}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}?api_key={}'.format(region, ppuid, api_token_var)

    respuesta = requests.get(api_url)

    if respuesta.status_code == 200:
        return json.loads(respuesta.content.decode('utf-8'))
    else:
        return print(respuesta.status_code)