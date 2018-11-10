class Character:
    def __init__(self, name, inventory, x, y, img):
        self.name = name
        self.inventory = inventory
        self.x = x
        self.y = y
        self.img = img

    # def move(self, dx, dy):
    #     if (self.x + dx) <= 0 or (self.x + dx) >= DISPLAY_W:
    #         dx = 0
    #     if (self.y + dy) <= 0 or (self.y + dy) >= DISPLAY_H:
    #         dy = 0
    #     self.x += dx
    #     self.y += dy

    def give_item(self, item):
        self.inventory.add(item)

    def drop_item(self, item):
        self.inventory.remove(item)