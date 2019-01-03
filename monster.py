class Monster:
    def __init__(self, id, name, health, dmg, item, x, y, img):
        self.id = id
        self.name = name
        self.base_health = health
        self.base_dmg = dmg
        self.item = item
        self.x = x
        self.y = y
        self.img = img
        self.health = health
