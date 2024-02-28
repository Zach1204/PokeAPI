import requests

#converts pokemon name to lower
def get_response(user_input: str) -> str: 
    lowered: str = user_input.lower()

    # Pulls lowered name into api
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{lowered}')
    
    #ported data from api into stats
    name = response.json()['forms'][0]['name']
    abilities = response.json()['abilities']
    abilities_info = []
    
    #takes in abilites and descriptions
    for ability in abilities:
            ability_name = ability['ability']['name']
            ability_url = ability['ability']['url']
            ability_description = requests.get(ability_url).json()['effect_entries'][1]['short_effect']
            abilities_info.append(f"__{ability_name}__: {ability_description}")


    #return
    if lowered == "":
        return 'Well well well'
    elif f'{name}' in lowered:
        return f'{name} and abilities:\n{"\n".join(abilities_info)}'