import json
import requests
from api_token import api_token_var_list
from ratelimit import limits, RateLimitException, sleep_and_retry

ONE_MINUTES = 60
MAX_CALLS_PER_MINUTE= 1000

@sleep_and_retry
@limits(calls=1, period= 1.4)
def get_name_and_tag_by_ppuid(region, ppuid, api_key):
    """"""
    api_url = 'https://{}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}?api_key={}'.format(region, ppuid, api_key)

    respuesta = requests.get(api_url)

    if respuesta.status_code == 200:
        return json.loads(respuesta.content.decode('utf-8'))
    else:
        return respuesta.status_code