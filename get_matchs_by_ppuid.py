import json
import requests
from api_token import api_token_var

def get_matchs_by_ppuid(ppuid, region):
    """Función que obtine una lista con los úñtimos 20 math de un jugador, dado su PPUID

    Args:
        ppuid (list): PPUI dado por riot games asociado a un gameName y un nameTag únicos
        region (list): región a la que pertenece el jugador (americas, europe, sea)

    Returns:
        list: lista con 20 strings alfanúmericas que corresponden a los 20 últimos mastches del jugador
    """

    api_url_base = 'https://{}.api.riotgames.com/lor/match/v1/matches/by-puuid/{}/ids?api_key={}'
    api_url = api_url_base.format(region, ppuid, api_token_var)

    respuesta = requests.get(api_url)

    if respuesta.status_code == 200:
        return json.loads(respuesta.content.decode('utf-8'))
    else:
        return print(respuesta.status_code)
