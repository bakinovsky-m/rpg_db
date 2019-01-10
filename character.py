class Character:
    def __init__(self, id, name, lvl, exp, health, dmg, inventory, x, y, location, img):
        self.id = id
        self.name = name
        self.base_health = health
        self.base_dmg = dmg
        self.inventory = inventory
        self.x = x
        self.y = y
        self.img = img
        self.curr_health = self.get_total_health()
        self.lvl = lvl
        self.exp = exp
        self.regeneration = 1
        self.curr_location = location

    def get_attack(self):
        return self.base_dmg + self.inventory.get_attack()

    def get_total_health(self):
        return self.base_health + self.inventory.get_health()

    def get_block(self):
        return self.inventory.get_block()

    def take_item(self, item):
        return self.inventory.add(item)

    def drop_item(self, item):
        self.inventory.remove(item)

    def regenerate(self):
        if self.curr_health < self.get_total_health():
            self.curr_health += self.regeneration