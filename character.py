class Character:
    def __init__(self, id, name, lvl, exp, health, dmg, inventory, x, y, img):
        self.id = id
        self.name = name
        self.base_health = health
        self.base_dmg = dmg
        self.inventory = inventory
        self.x = x
        self.y = y
        self.img = img
        self.health = health
        self.lvl = lvl
        self.exp = exp

    def get_attack(self):
        return self.base_dmg + self.inventory.get_attack()


    def take_item(self, item):
        return self.inventory.add(item)

    def drop_item(self, item):
        self.inventory.remove(item)