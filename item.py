class Item:
    def __init__(self, name, attack=0, defense=0, img=None):
        if attack < 0 or defense < 0:
            raise Exception("Item can't have neg attack or defense")
        if attack > 0 and defense > 0:
            raise Exception("Item can't be both attacking and defending")

        self.name = name
        self.attack = attack
        self.defense = defense
        self.img = img