from constants import hex_to_rgb

class Location:
    def __init__(self, id_, name, x, y, h):
        self.id = id_
        self.name = name
        self.x = x
        self.y = y
        self.hex = h
        self.rgb = hex_to_rgb(self.hex)