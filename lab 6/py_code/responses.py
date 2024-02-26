import requests

def get_response(user_input: str) -> str: 
    lowered: str = user_input.lower()

    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{lowered}')
    name = response.json()['forms'][0]['name']
    ability = response.json()['abilities'][0]['ability']['name']

    if lowered == "":
        return 'Well well well'
    elif f'{name}' in lowered:
        return f'{name} and {ability}' 