class Move:
    def __init__(self, name, power, type, damage_type) -> None:
        self.name = name
        self.power = power
        self.type = type
        #physical, special, status
        self.damage_type = damage_type