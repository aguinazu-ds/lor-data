import json
import requests
from api_token import api_token_var

def get_player_puuid(region, gameName, tagLine):
    """Función que entrega como resultado el PUUID de una cuenta de Riot, dado la region, el gameName y el tag del usuario (Ej. americas, Bast, 8341)

    Args:
        region (string): String con el nombre de la region del servidor donde pertenece la cuenta. Los únicos input válidos son americas, europe y sea 
        gameName (string): Nickname que el usuario usa en su cuenta de riot
        tagLine (string): String con el tag asociado al nombre de usuario. Este puede ser solo números, solo letras o letras y números (Ej. '8431', 'HDR', 'EZ44')

    Returns:
        string: string que contiene el PUUID asociado al gameName y el tagLine
    """
    
    api_url_base = 'https://{}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'
    api_url = '{}{}/{}?api_key={}'.format(api_url_base.format(region), gameName, tagLine, api_token_var)

    respuesta = requests.get(api_url)

    if respuesta.status_code == 200:
        return json.loads(respuesta.content.decode('utf-8'))['puuid']
    else:
        return None