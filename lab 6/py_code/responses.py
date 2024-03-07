import requests
from discord import Embed

#Pokemon evolution chain 
def get_evolution_chain(pokemon_name: str) -> str:
    lowered = pokemon_name.lower()

    response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{lowered}/')
    species_data = response.json()

    if 'evolution_chain' not in species_data:
        return None

    evolution_chain_url = species_data['evolution_chain']['url']
    evolution_chain_response = requests.get(evolution_chain_url)
    evolution_chain_data = evolution_chain_response.json()

    evolution_tree = []
    current_evolution = evolution_chain_data['chain']
    while True:
        evolution_tree.append(current_evolution['species']['name'].capitalize())
        if not current_evolution['evolves_to']:
            break
        current_evolution = current_evolution['evolves_to'][0]
    
    return ' -> '.join(evolution_tree)

#converts pokemon name to lower
def get_response(user_input: str) -> str: 
    lowered: str = user_input.lower()

    # Pulls lowered name into api
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{lowered}')
    
    #ported data from api into stats
    pokemon_data = response.json()
    name = pokemon_data['forms'][0]['name'].capitalize()
    abilities = pokemon_data['abilities']
    abilities_info = []
    base_stats = pokemon_data['stats']
    sprite_url = pokemon_data['sprites']['front_default']
    
    #takes in abilites and descriptions
    for ability in abilities:
            ability_name = ability['ability']['name'].capitalize()
            ability_url = ability['ability']['url']
            ability_description = requests.get(ability_url).json()['effect_entries'][1]['short_effect']
            
            if ability['is_hidden']:
                isHidden = '(*Hidden*)'
            else:
                isHidden = ''
                
            if ability_name == 'Overgrow':
                ability_description = "Powers up Grass-type moves when the Pokémon's HP is low."
            abilities_info.append(f"{isHidden} __{ability_name}__: {ability_description}")
        
    evolution_tree = get_evolution_chain(name)
    if evolution_tree:
        abilities_info.append(f"__Evolution__: {evolution_tree}")

    #results!
    info = Embed(title=name)
    
    info.set_image(url=sprite_url)
    
    info.add_field(name="Abilities:", value="\n".join(abilities_info), inline=True)
    
    for stat in base_stats:
        stat_name = stat['stat']['name'].capitalize()  # Capitalize stat name
        stat_value = stat['base_stat']
        info.add_field(name=stat_name, value=stat_value, inline=False)
    
    
    return info 
