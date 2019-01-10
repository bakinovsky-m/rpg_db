DISPLAY_W = 1200
DISPLAY_H = 1000
MAP_W = 900
MAP_H = 1000
FPS = 30
BACKGROUND_COLOR = (0, 50, 0)
INVENTORY_COLOR = (197,180,160)
TEXT_COLOR = (0,0,0)
TEXT_SIZE = 30
TILE_SIZE = 100

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))
