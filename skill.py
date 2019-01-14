class Skill:
    def __init__(self, id, name, cost, dmg, on_self, lvl_impr, type_, duration, asset):
        self.id = id
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.on_self = on_self
        self.lvl_impr = lvl_impr
        self.type = type_
        self.duration = duration
        self.img = asset

    def use_on_target(self, target):
        if self.type == 'heal':
            target.curr_health += self.dmg
            if target.curr_health >= target.get_total_health():
                target.curr_health = target.get_total_health()
        if self.type == 'dmg':
            target.health -= self.dmg
