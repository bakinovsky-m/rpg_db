import pygame

class Item:
    def __init__(self, id, name, asset=None, attack=0, defense=0, hp=0):
        self.id = id
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.asset = asset
        if asset != None:
            self.img = pygame.image.load(asset)
        self.x = -1
        self.y = -1

    def get_value(self):
        return self.attack + self.defense + self.hp