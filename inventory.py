from pypika import Table, Query
from item import Item

class Inventory:
    def __init__(self, id, capacity, size, db):
        self.id = id
        self.items = []
        self.size = size
        self.capacity = capacity
        self.db = db

        t = Table('items_in_inventory')
        q = Query.from_(t).select('*').where(t.inv == self.id).get_sql()
        res = self.db.select(q)
        for i in res:
            t = Table('items')
            q = Query.from_(t).select('*').where(t.id == i[1]).get_sql()
            r = self.db.select(q)
            # id name dmg hp  block asset
            r = r[0]
            self.items.append(Item(r[0], r[1], r[5], r[2], r[4], r[3]))


    def add(self, item):
        if self.size == self.capacity:
            return False

        self.size += 1
        self.items.append(item)

        t = Table('items_in_inventory')
        q = Query.into(t).insert(self.id, item.id).get_sql()
        self.db.insert(q)
        t = Table('inventories')
        q = Query.update(t).set(t.size, self.size).where(t.id == self.id).get_sql()
        self.db.update(q)
        return True


    def remove(self, item):
        self.size -= 1
        # self.items = [it for it in self.items if it.name != item.name]
        self.items = [it for it in self.items if it != item]
        t = Table('items_in_inventory')
        q = Query.from_(t).delete().where(t.inv == self.id).where(t.item == item.id).get_sql()
        self.db.update(q)

    def get_attack(self):
        res = 0
        for i in self.items:
            res += i.attack
        return res

    def get_block(self):
        res = 0
        for i in self.items:
            res += i.defense
        return res

    def get_health(self):
        res = 0
        for i in self.items:
            res += i.hp
        return res
