import random   
import requests
import math

def calc_hp(base_hp, iv, ev, lvl):
    return math.floor( ((2 * base_hp + iv + math.floor(ev / 4)) * lvl) / 100) + lvl + 10

#nature: 1.1 for positive, 1 for neutral, 0.9 for negative
def calc_stat(base_stat, iv, ev, lvl, nature): 
    return (math.floor( ((2 * base_stat + iv + math.floor(ev / 4)) * lvl) / 100) + 5) * nature

class Pokemon:
    def __init__(self, name, type1, type2, level, base_hp, base_attack, base_defense, base_speed) -> None:
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.level = level
        self.hp = base_hp
        self.attack = base_attack
        self.defense = base_defense
        self.speed = base_speed

    def __str__(self) -> str:
        return f"{self.name}: hp: {self.hp}"

    def display(self):
        print(self.name.capitalize()+":")
        print(f"\t{self.type1.capitalize()}", end="")
        print(f"/{self.type2.capitalize()}") if self.type2 else print()
        print(f"\tLVL:\t{self.level}")
        print(f"\tHP:\t{self.hp}")
        print(f"\tATK:\t{self.attack}")
        print(f"\tDEF:\t{self.defense}")
        print(f"\tSPE:\t{self.speed}")

    def take_damage(self, damage):
        self.hp -= damage

def get_damage_multiplier(attacking, defending):
    attacking_type = random.choice([attacking.type1,attacking.type2]) if attacking.type2 else attacking.type1
    defending_type_1 = defending.type1
    multiplier = typeChart[type_order.index(attacking_type)][type_order.index(defending_type_1)]
    if defending.type2:
        multiplier *= typeChart[type_order.index(attacking_type)][type_order.index(defending.type2)]
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
    if(faster_pokemon.hp <= 0):
        print(f"{slower_pokemon.name} Wins!")
        return
    elif(slower_pokemon.hp <= 0):
        print(f"{faster_pokemon.name} Wins!")
        return
    else:
        damage = attack(faster_pokemon, slower_pokemon)
        print(faster_pokemon)
        print(slower_pokemon)
        slower_pokemon.take_damage(damage)
        print(f"{faster_pokemon.name} attacks {slower_pokemon.name} for {damage} damage!")
    if(faster_pokemon.hp <= 0):
        print(f"{slower_pokemon.name} Wins!")
        return
    elif(slower_pokemon.hp <= 0):
        print(f"{faster_pokemon.name} Wins!")
        return
    else:
        damage = attack(slower_pokemon, faster_pokemon)
        print(faster_pokemon)
        print(slower_pokemon)
        faster_pokemon.take_damage(damage)
        print(f"{slower_pokemon.name} attacks {faster_pokemon.name} for {damage} damage!")
        fight(faster_pokemon, slower_pokemon)

def create_pokemon(pokemon_name):
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
    poke = Pokemon(pokemon_name, type_1, type_2, level, base_hp, base_atk, base_def, base_spe)
    return poke


type_order = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]
typeChart = [
    # no  fi  wa  el  gr  ic  fi  po  gr  fl  ps  bu  ro  gh  dr  da  st  fa
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,0.5,  0,  1,  1,0.5,  1],
    [  1,0.5,0.5,  1,  2,  2,  1,  1,  1,  1,  1,  2,0.5,  1,0.5,  1,  2,  1],
    [  1,  2,0.5,  1,0.5,  1,  1,  1,  2,  1,  1,  1,  2,  1,0.5,  1,  1,  1],
    [  1,  1,  2,0.5,0.5,  1,  1,  1,  0,  2,  1,  1,  1,  1,0.5,  1,  1,  1],
    [  1,0.5,  2,  1,0.5,  1,  1,0.5,  2,0.5,  1,0.5,  2,  1,0.5,  1,0.5,  1],
    [  1,0.5,0.5,  1,  2,0.5,  1,  1,  2,  2,  1,  1,  1,  1,  2,  1,0.5,  1],
    [  2,  1,  1,  1,  1,  2,  1,0.5,  1,0.5,0.5,0.5,  2,  0,  1,  2,  2,0.5],
    [  1,  1,  1,  1,  2,  1,  1,0.5,0.5,  1,  1,  1,0.5,0.5,  1,  1,  0,  2],
    [  1,  2,  1,  2,0.5,  1,  1,  2,  1,  0,  1,0.5,  2,  1,  1,  1,  2,  1],
    [  1,  1,  1,0.5,  2,  1,  2,  1,  1,  1,  1,  2,0.5,  1,  1,  1,0.5,  1],
    [  1,  1,  1,  1,  1,  1,  2,  2,  1,  1,0.5,  1,  1,  1,  1,  0,0.5,  1],
    [  1,0.5,  1,  1,  2,  1,0.5,0.5,  1,0.5,  2,  1,  1,0.5,  1,  2,0.5,0.5],
    [  1,  2,  1,  1,  1,  2,0.5,  1,0.5,  2,  1,  2,  1,  1,  1,  1,0.5,  1],
    [  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  1,  1,  2,  1,0.5,  1,  1],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  1,0.5,  0],
    [  1,  1,  1,  1,  1,  1,0.5,  1,  1,  1,  2,  1,  1,  2,  1,0.5,  1,0.5],
    [  1,0.5,0.5,0.5,  1,  2,  1,  1,  1,  1,  1,  1,  2,  1,  1,  1,0.5,  2],
    [  1,0.5,  1,  1,  1,  1,  2,0.5,  1,  1,  1,  1,  1,  1,  2,  2,0.5,  1],
    ]

# p1 = Pokemon("Golem",   "Rock",     "Ground",   100, 126, 372, 359, 302)
# p2 = Pokemon("Durant",  "Bug",      "Steel",    100, 254, 348, 323, 258)
# p3 = Pokemon("Wailord", "Water",    None,       100, 156, 279, 189, 482)
# p4 = Pokemon("Pikachu", "Electric", None,       100, 216, 229, 179, 212)

# fight(p4, p2)
pokemon_1 = create_pokemon("golem")
pokemon_2 = create_pokemon("durant")
pokemon_3 = create_pokemon("wailord")
pokemon_4 = create_pokemon("pikachu")
pokemon_1.display()
pokemon_4.display()