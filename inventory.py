MAX_SIZE = 10

class Inventory:
    def __init__(self):
        self.items = []
        self.size = 0
        self.capacity = MAX_SIZE

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items = [it for it in self.items if it.name != item.name]