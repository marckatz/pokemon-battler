import random   
import requests
import math
from pokedata import TYPE_CHART as type_chart, TYPE_ORDER as type_order, NATURES as natures

def calc_hp(base_hp, iv, ev, lvl):
    return math.floor( ((2 * base_hp + iv + math.floor(ev / 4)) * lvl) / 100) + lvl + 10

#nature: 1.1 for positive, 1 for neutral, 0.9 for negative
def calc_stat(base_stat, iv, ev, lvl, nature): 
    return math.floor((math.floor( ((2 * base_stat + iv + math.floor(ev / 4)) * lvl) / 100) + 5) * nature)

class Pokemon:
    #name, type1, nature: String; type2: String or None, level, base_{stat}: int, iv_spread, ev_spread:[int]
    def __init__(self, name, type1, type2, level, base_hp, base_attack, base_defense, base_speed, iv_spread, ev_spread, nature) -> None:
        nature_multipliers = natures[nature]

        max_hp = calc_hp(base_hp, iv_spread[0], ev_spread[0], level)
        atk = calc_stat(base_attack, iv_spread[1], ev_spread[1], level, nature_multipliers[1])
        df = calc_stat(base_defense, iv_spread[2], ev_spread[2], level, nature_multipliers[2])
        spe = calc_stat(base_speed, iv_spread[5], ev_spread[5], level, nature_multipliers[5])
        
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.level = level
        self.max_hp = max_hp
        self.current_hp = self.max_hp
        self.attack = atk
        self.defense = df
        self.speed = spe

    def __str__(self) -> str:
        return f"{self.name}: hp: {self.current_hp}/{self.max_hp}"

    def display(self):
        print(self.name.capitalize()+":")
        print(f"\t{self.type1.capitalize()}", end="")
        print(f"/{self.type2.capitalize()}") if self.type2 else print()
        print(f"\tLVL:\t{self.level}")
        print(f"\tHP:\t{self.max_hp}")
        print(f"\tATK:\t{self.attack}")
        print(f"\tDEF:\t{self.defense}")
        print(f"\tSPE:\t{self.speed}")

    def take_damage(self, damage):
        self.current_hp -= damage

def get_damage_multiplier(attacking, defending):
    attacking_type = random.choice([attacking.type1,attacking.type2]) if attacking.type2 else attacking.type1
    defending_type_1 = defending.type1
    multiplier = type_chart[type_order.index(attacking_type)][type_order.index(defending_type_1)]
    if defending.type2:
        multiplier *= type_chart[type_order.index(attacking_type)][type_order.index(defending.type2)]
    return multiplier

def attack(attacking, defending):
    power = 60
    damage_multiplier = get_damage_multiplier(attacking, defending)
    damage = ((((((2 * attacking.level) / 5) + 2) * power * (attacking.attack/defending.defense)) / 50) + 2)
    damage *= damage_multiplier
    damage *= (random.randint(85,100) / 100)
    return round(damage)

def fight(pokemon1, pokemon2):
    faster_pokemon, slower_pokemon = (pokemon1, pokemon2) if pokemon1.speed > pokemon2.speed else (pokemon2, pokemon1)
    if(faster_pokemon.current_hp <= 0):
        print(f"{slower_pokemon.name.capitalize()} Wins!")
        return
    elif(slower_pokemon.current_hp <= 0):
        print(f"{faster_pokemon.name.capitalize()} Wins!")
        return
    else:
        damage = attack(faster_pokemon, slower_pokemon)
        print(faster_pokemon)
        print(slower_pokemon)
        slower_pokemon.take_damage(damage)
        print(f"{faster_pokemon.name.capitalize()} attacks {slower_pokemon.name.capitalize()} for {damage} damage!")
    if(faster_pokemon.current_hp <= 0):
        print(f"{slower_pokemon.name.capitalize()} Wins!")
        return
    elif(slower_pokemon.current_hp <= 0):
        print(f"{faster_pokemon.name.capitalize()} Wins!")
        return
    else:
        damage = attack(slower_pokemon, faster_pokemon)
        print(faster_pokemon)
        print(slower_pokemon)
        faster_pokemon.take_damage(damage)
        print(f"{slower_pokemon.name.capitalize()} attacks {faster_pokemon.name.capitalize()} for {damage} damage!")
        fight(faster_pokemon, slower_pokemon)

def create_pokemon(pokemon_name):
    max_iv_spread = [31,31,31,31,31,31]
    #4 hp, max atk, max def, 0 rest
    ev_spread = [4, 252, 252, 0, 0, 0]
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    poke_json = response.json()
    types = poke_json["types"]
    type_1 = types[0]["type"]["name"]
    type_2 = None if len(types) == 1 else types[1]["type"]["name"]
    level = 100
    stats = poke_json["stats"]
    base_hp  = stats[0]["base_stat"]
    base_atk = stats[1]["base_stat"]
    base_def = stats[2]["base_stat"]
    base_spa = stats[3]["base_stat"]
    base_spd = stats[4]["base_stat"]
    base_spe = stats[5]["base_stat"]
    poke = Pokemon(pokemon_name, type_1, type_2, level, base_hp, base_atk, base_def, base_spe, max_iv_spread, ev_spread, "lonely")
    return poke

# p1 = Pokemon("Golem",   "Rock",     "Ground",   100, 126, 372, 359, 302)
# p2 = Pokemon("Durant",  "Bug",      "Steel",    100, 254, 348, 323, 258)
# p3 = Pokemon("Wailord", "Water",    None,       100, 156, 279, 189, 482)
# p4 = Pokemon("Pikachu", "Electric", None,       100, 212, 209, 179, 216)

# fight(p4, p2)
pokemon_1 = create_pokemon("golem")
pokemon_2 = create_pokemon("durant")
pokemon_3 = create_pokemon("wailord")
pokemon_4 = create_pokemon("pikachu")
pokemon_2.display()
pokemon_3.display()
fight(pokemon_2, pokemon_3)