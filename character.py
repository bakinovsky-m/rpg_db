class Character:
    def __init__(self, id, name, lvl, exp, health, dmg, inventory, x, y, location, img):
        self.id = id
        self.name = name
        self.start_health = health
        self.start_dmg = dmg
        self.lvl = lvl
        self.base_health = self.start_health * self.lvl
        self.base_dmg = self.start_dmg * self.lvl
        self.inventory = inventory
        self.x = x
        self.y = y
        self.img = img
        self.curr_health = self.get_total_health()
        self.exp = exp
        self.regeneration = self.lvl
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

    def recalculate_basics(self):
        self.base_health = self.start_health * self.lvl
        self.base_dmg = self.start_dmg * self.lvl
        self.regeneration = self.lvl
