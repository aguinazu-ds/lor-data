from codecs import ignore_errors
import json
import requests
from ratelimit import limits
from api_token import api_token_var

TWO_MINUTES = 120

@limits(calls=100, period= TWO_MINUTES)
def get_match_info_by_id(region, match_id):
    """"""
    api_url_base = 'https://{}.api.riotgames.com/lor/match/v1/matches/{}?api_key={}'
    api_url = api_url_base.format(region, match_id, api_token_var)

    respuesta = requests.get(api_url)

    if respuesta.status_code == 200:
        return json.loads(respuesta.content.decode('utf-8'))
    else:
        raise Exception('API response: {}'.format(respuesta.status_code))

#print(get_match_info_by_id('americas', '6ce11b6c-fb64-433d-97f1-511a606f94b4'))
# l = [
#     "0c79da86-5de2-41c8-8788-5e1f32a31853",
#     "261c89e8-e7ce-42d7-9748-4fb8e2c7eab8",
#     "cb407b71-5d2c-495c-8df7-3f8b7432a9b6",
#     "93c0645d-2bdb-45ba-9795-ee7a1e5e7b4c",
#     "6e1b82fd-3a78-456f-bbd6-add8d11c3ebb",
#     "3c4b0afa-38a1-4504-a200-d47d04556c43",
#     "485e05bd-739c-40f0-a68a-7cb574fef3d7",
#     "16accadb-702e-4782-adfd-54bad08415a0",
#     "b6ce7d9e-6858-4397-92ab-d60f4953c9bd",
#     "f31c3529-029e-4744-98dd-3930295095d9",
#     "c477c6f2-a36f-4768-9945-d6f1bfe816f9",
#     "19298346-92d9-4547-8d9e-46e3d2b0e23d",
#     "4ee540ad-56b2-4bb1-a353-acc2e2ad42a3",
#     "1de1d964-6943-4c91-aaed-385f7a60b352",
#     "b498b2d2-d697-48b0-97ee-e75a8cbbb757",
#     "52c692d9-1a8f-4109-a8fc-3eea51c173bb",
#     "ef9a1189-3d30-409f-af03-5d34a4868f1d",
#     "58133071-db77-4ca0-9fa0-5c43ea06b8fd",
#     "10e56826-c8a2-4fe3-9e3e-d00de937345c",
#     "1de1d01a-5cab-46cd-a740-972930626405"
# ]

# l = [
#     "9a12e849-7943-4751-a895-80430029e53e",
#     "21ebab97-cd12-43ec-b2a4-a913f13c3085",
#     "b4cebb88-4795-4a21-9d09-35814de6893e",
#     "11925b8a-bb04-41fd-9516-c8bba52040e0",
#     "4f16dc44-3aef-496f-b81b-e5dc84c87167",
#     "002278f0-2bf6-4e25-a4fe-d563feff45e6",
#     "ba18689c-6186-4d31-9a29-c190bb819925",
#     "55ca29a7-62f7-4749-a73d-918f28bc6937",
#     "2776d762-0852-48e1-b40b-b953c065c58c",
#     "b74d740a-a838-4706-a533-e76562f17ee0",
#     "1036e00b-52a8-4426-8479-87ef8685550a",
#     "b66a3fc8-40c2-4845-baee-8512fd9c57ce",
#     "77e78074-e965-4ba6-a69c-5f1510e07730",
#     "b79f9d4c-b68d-483c-b300-c2a0f56ef6ec",
#     "fc80a131-8cd0-4823-a2be-6ed695feeff9",
#     "9a1b3500-b132-4911-b402-1a626aa8fa50",
#     "ad4eb707-1d73-4fcb-88ef-845d214b1230",
#     "52bb1ee3-5795-498c-a339-a959ee0ca9aa",
#     "f4269bc4-ebac-4e5f-ab0d-d49025bac33c",
#     "96bd0a35-3d4d-4bce-8790-5fe22ee81702"
# ]

# for match in l: 
#     print(get_match_info_by_id('americas', match)['info']['game_mode'])
