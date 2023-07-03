import random   
import requests
import math
from pokedata import TYPE_CHART as type_chart, TYPE_ORDER as type_order, NATURES as natures
from move import Move as Move

def calc_hp(base_hp, iv, ev, lvl):
    return math.floor( ((2 * base_hp + iv + math.floor(ev / 4)) * lvl) / 100) + lvl + 10

#nature: 1.1 for positive, 1 for neutral, 0.9 for negative
def calc_stat(base_stat, iv, ev, lvl, nature): 
    return math.floor((math.floor( ((2 * base_stat + iv + math.floor(ev / 4)) * lvl) / 100) + 5) * nature)

class Pokemon:
    #name, type1, nature: String; type2: String or None; level, base_{stat}: int; iv_spread, ev_spread:[int]
    def __init__(self, name, type1, type2, level, 
                 base_hp, base_attack, base_defense, base_spa, base_spd, base_speed, 
                 iv_spread, ev_spread, nature) -> None:
        nature_multipliers = natures[nature]

        max_hp = calc_hp(base_hp, iv_spread[0], ev_spread[0], level)
        atk = calc_stat(base_attack, iv_spread[1], ev_spread[1], level, nature_multipliers[1])
        df = calc_stat(base_defense, iv_spread[2], ev_spread[2], level, nature_multipliers[2])
        spa = calc_stat(base_spa, iv_spread[3], ev_spread[3], level, nature_multipliers[3])
        spd = calc_stat(base_spd, iv_spread[4], ev_spread[4], level, nature_multipliers[4])
        spe = calc_stat(base_speed, iv_spread[5], ev_spread[5], level, nature_multipliers[5])
        
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.level = level
        self.max_hp = max_hp
        self.current_hp = self.max_hp
        self.attack = atk
        self.defense = df
        self.special_atk = spa
        self.special_def = spd
        self.speed = spe
        self.moves = []

    #can take move name or id
    def add_move(self, move):
        if len(self.moves) >= 4:
            print("Too many moves")
            pass
        else:
            name, power, move_type, damage_type = get_move(move)
            self.moves.append(Move(name, power, move_type, damage_type))

    def __str__(self) -> str:
        return f"{self.name.capitalize()}: hp: {self.current_hp}/{self.max_hp}"

    def display(self):
        print(self.name.capitalize()+":")
        print(f"\t{self.type1.capitalize()}", end="")
        print(f"/{self.type2.capitalize()}") if self.type2 else print()
        print(f"\tLVL:\t{self.level}")
        print(f"\tHP:\t{self.max_hp}")
        print(f"\tATK:\t{self.attack}")
        print(f"\tDEF:\t{self.defense}")
        print(f"\tSPA:\t{self.special_atk}")
        print(f"\tSPD:\t{self.special_def}")
        print(f"\tSPE:\t{self.speed}")
        print("Moves:")
        for move in self.moves:
            print("\t"+move.name.capitalize())

    def take_damage(self, damage):
        self.current_hp -= damage

def get_damage_multiplier(attacking, defending):
    attacking_type = random.choice([attacking.type1,attacking.type2]) if attacking.type2 else attacking.type1
    defending_type_1 = defending.type1
    multiplier = type_chart[type_order.index(attacking_type)][type_order.index(defending_type_1)]
    if defending.type2:
        multiplier *= type_chart[type_order.index(attacking_type)][type_order.index(defending.type2)]
    return multiplier

def attack(attacking, defending, damage_multiplier):
    power = 60
    if attacking.attack > attacking.special_atk:
        damage = ((((((2 * attacking.level) / 5) + 2) * power * (attacking.attack/defending.defense)) / 50) + 2)
    else:
        damage = ((((((2 * attacking.level) / 5) + 2) * power * (attacking.special_atk/defending.special_def)) / 50) + 2)
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
        damage_multiplier = get_damage_multiplier(faster_pokemon, slower_pokemon)
        damage = attack(faster_pokemon, slower_pokemon, damage_multiplier)
        print(faster_pokemon)
        print(slower_pokemon)
        slower_pokemon.take_damage(damage)
        print(f"{faster_pokemon.name.capitalize()} attacks {slower_pokemon.name.capitalize()} for {damage} damage!")
        if damage_multiplier > 1:
            print("It's super effective!")
        elif damage_multiplier < 1:
            print("It's not very effective")
    if(faster_pokemon.current_hp <= 0):
        print(f"{slower_pokemon.name.capitalize()} Wins!")
        return
    elif(slower_pokemon.current_hp <= 0):
        print(f"{faster_pokemon.name.capitalize()} Wins!")
        return
    else:
        damage_multiplier = get_damage_multiplier(slower_pokemon, faster_pokemon)
        damage = attack(slower_pokemon, faster_pokemon, damage_multiplier)
        print(faster_pokemon)
        print(slower_pokemon)
        faster_pokemon.take_damage(damage)
        print(f"{slower_pokemon.name.capitalize()} attacks {faster_pokemon.name.capitalize()} for {damage} damage!")
        if damage_multiplier > 1:
            print("It's super effective!")
        elif damage_multiplier < 1:
            print("It's not very effective")
        fight(faster_pokemon, slower_pokemon)

def get_move(move_name):
    url = f"https://pokeapi.co/api/v2/move/{move_name}"
    response = requests.get(url)
    poke_json = response.json()
    move_type = poke_json["type"]["name"]
    power = poke_json["power"]
    name = poke_json["name"]
    damage_type = poke_json["damage_class"]["name"]
    # print(f"{move_name.capitalize()}: {power}, {move_type}")
    return name, power, move_type, damage_type

def create_pokemon(pokemon_name):
    max_iv_spread = [31,31,31,31,31,31]
    #4 hp, max atk, max spa, 0 rest
    ev_spread = [4, 252, 0, 252, 0, 0]
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
    poke = Pokemon(pokemon_name, type_1, type_2, level, 
                   base_hp, base_atk, base_def, base_spa, base_spd, base_spe, 
                   max_iv_spread, ev_spread, "hardy")
    return poke

pokemon_1 = create_pokemon("golem")
pokemon_2 = create_pokemon("durant")
pokemon_3 = create_pokemon("wailord")
pokemon_4 = create_pokemon("pikachu")


pokemon_4.add_move("thunderbolt")
pokemon_4.add_move("tackle")
pokemon_4.add_move("surf")
pokemon_4.add_move("psychic")


# pokemon_2.display()
pokemon_4.display()

# fight(pokemon_2, pokemon_3)
