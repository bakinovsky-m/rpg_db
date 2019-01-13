import pygame
import pypika

from character import Character
from monster import Monster
from inventory import Inventory
from db_handler import DBHandler
from item import Item
from map import Map
from location import Location

# from constants import DISPLAY_H, DISPLAY_W, BACKGROUND_COLOR, TILE_SIZE, FPS, MAP_H, MAP_W, INVENTORY_COLOR, TEXT_COLOR
from constants import *
import constants

INV_H = 0
CUR_ITEM = 0

LOCATIONS = []
CUR_LOCATION = None

def move(char, mmap, dx, dy):
    if not mmap.is_ok_move(char, dx, dy):
        print('no way')
        return
    index = (char.x + dx) + (char.y + dy)*mmap.w
    mmmap = mmap.cells[index]
    if mmmap != 0:
        if isinstance(mmmap, Monster):
            monst = mmmap
            print('before fight')
            print('char health', char.curr_health)
            print('monst health', monst.health)
            char.curr_health -= monst.base_dmg - char.inventory.get_block()
            monst.health -= char.get_attack()
            if monst.health <= 0:
                mmap.cells[index] = monst.item
                monst.item.x = monst.x
                monst.item.y = monst.y
            print('after fight')
            print('char health', char.curr_health)
            print('monst health', monst.health)
        elif isinstance(mmmap, Item):
            if char.take_item(mmmap):
                mmmap.x = -1
                mmmap.y = -1
                mmap.cells[index] = 0
            char.x += dx
            char.y += dy

    else:
        char.x += dx
        char.y += dy

def draw_UI(screen, hero, in_inventory_mode):
    f = pygame.font.SysFont('Noto Mono', TEXT_SIZE)

    INFO_BAR = []

    INFO_BAR.append(f.render(hero.name, False, TEXT_COLOR))
    s = 'lvl: ' + str(hero.lvl) + '  exp: ' + str(hero.exp)
    INFO_BAR.append(f.render(s, False, TEXT_COLOR))
    s = 'hp: ' + str(hero.curr_health) + '/' + str(hero.get_total_health()) + '(+' + str(hero.inventory.get_health()) + ')' + ' reg:' + str(hero.regeneration)
    INFO_BAR.append(f.render(s, False, TEXT_COLOR))
    s = 'dmg: ' + str(hero.base_dmg) + '(+' + str(hero.inventory.get_attack()) + ')'
    INFO_BAR.append(f.render(s, False, TEXT_COLOR))
    s = 'blk: ' + str(hero.get_block())
    INFO_BAR.append(f.render(s, False, TEXT_COLOR))

    i = 0
    for a in INFO_BAR:
        screen.blit(a, (MAP_W, i * TEXT_SIZE))
        i += 1

    screen.blit(f.render('--------------', False, TEXT_COLOR), (MAP_W, i * TEXT_SIZE))
    i += 1

    s = 'inventory: ' + str(hero.inventory.size) + "/" + str(hero.inventory.capacity)
    screen.blit(f.render(s, False, TEXT_COLOR), (MAP_W, i * TEXT_SIZE))
    i += 1

    global INV_H
    INV_H = i * TEXT_SIZE

    INV_BAR = []

    for it in hero.inventory.items:
        INV_BAR.append(f.render(it.name + ' (a:' + str(it.attack) + ',b:' + str(it.defense) + ',h:' + str(it.hp) + ')', False, TEXT_COLOR))

    cur_item = 0
    for a in INV_BAR:
        screen.blit(a, (MAP_W, i * TEXT_SIZE))
        if cur_item == CUR_ITEM:
            surf = pygame.Surface((10, 10))
            surf.fill((255,0,0))
            screen.blit(surf, (DISPLAY_W - 10, i*TEXT_SIZE))
        i += 1
        cur_item += 1

def init_locations(db_handler):
    t = pypika.Table('locations')
    q = pypika.Query.from_(t).select('*').get_sql()

    response = db_handler.select(q)

    for r in response:
        LOCATIONS.append(Location(r[0], r[1], r[2], r[3], r[4]))

def make_pygame_image(path):
    return pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE))

def main():
    # INIT
    db = DBHandler()

    print('input the name: ')
    # hero_name = input()
    hero_name = 'Dragonborn'
    t = pypika.Table('characters')
    q = pypika.Query.from_(t).select('*').where(t.name == hero_name).get_sql()
    hero_res = db.select(q)
    # id name lvl curr_exp base_health base_damage curr_location inventory 
    try:
        hero_res = hero_res[0]
    except IndexError:
        print('no such character')
        return

    # INVENTORY
    t = pypika.Table('inventories')
    q = pypika.Query.from_(t).select('*').where(t.id == hero_res[7]).get_sql()
    # id capacity size
    inv_res = db.select(q)[0]
    heros_inv = Inventory(inv_res[0], inv_res[1], inv_res[2], db)

    # MONSTERS
    t = pypika.Table('monsters')
    q = pypika.Query.from_(t).select('*').get_sql()
    monster_res = db.select(q)
    monsters = []
    # id name lvl base_health base_damage curr_location item asset
    for mr in monster_res:
        t = pypika.Table('items')
        q = pypika.Query.from_(t).select('*').where(t.id == mr[6]).get_sql()
        rrr = db.select(q)[0]
        item_to_monst = Item(rrr[0], rrr[1], make_pygame_image(rrr[5]), rrr[2], rrr[4], rrr[3])
        monsters.append(Monster(mr[0], mr[1], mr[3], mr[4], item_to_monst, 0, 0, make_pygame_image(mr[7])))

    # LOCATIONS
    init_locations(db)
    for l in LOCATIONS:
        if l.id == hero_res[6]:
            global CUR_LOCATION
            CUR_LOCATION = l

    # PYGAME
    pygame.init()
    pygame.key.set_repeat(100, 300)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([DISPLAY_W, DISPLAY_H], pygame.DOUBLEBUF)

    mapp = Map(MAP_W, MAP_H)
    mapp.random_fill(monsters, 2)

    hero = Character(hero_res[0], hero_res[1], hero_res[2], hero_res[3], hero_res[4], hero_res[5], heros_inv, round(mapp.w/2), round(mapp.h/2), CUR_LOCATION, make_pygame_image("assets/new_hero.png"))

    constants.BACKGROUND_COLOR = hero.curr_location.rgb

    inventory_surf = pygame.Surface((DISPLAY_W - MAP_W, DISPLAY_H))
    inventory_surf.fill(INVENTORY_COLOR)

    in_inventory_mode = False
    screen.fill(constants.BACKGROUND_COLOR)
    for i, it in mapp:
        if it != 0:
            screen.blit(it.img, (it.x * TILE_SIZE, it.y * TILE_SIZE))
    screen.blit(hero.img, (hero.x * TILE_SIZE, hero.y * TILE_SIZE))
    screen.blit(inventory_surf, (MAP_W,0))
    draw_UI(screen, hero, in_inventory_mode)
    pygame.display.update()

    running = True
    while running:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                    break
                if e.key == pygame.K_i:
                    # print(hero.x, hero.y)
                    in_inventory_mode = not in_inventory_mode
                    # break

                if not in_inventory_mode:
                    if e.key == pygame.K_UP:
                        move(hero, mapp, 0, -1)
                    if e.key == pygame.K_DOWN:
                        move(hero, mapp, 0, 1)
                    if e.key == pygame.K_LEFT:
                        move(hero, mapp, -1, 0)
                    if e.key == pygame.K_RIGHT:
                        move(hero, mapp, 1, 0)

                    hero.regenerate()

                else:
                    global CUR_ITEM
                    if e.key == pygame.K_UP:
                        if CUR_ITEM != 0:
                            CUR_ITEM -= 1
                    if e.key == pygame.K_DOWN:
                        if CUR_ITEM < hero.inventory.size - 1:
                            CUR_ITEM += 1
                    if e.key == pygame.K_d:
                        hero.drop_item(hero.inventory.items[CUR_ITEM])
                        print(len(hero.inventory.items))

                screen.fill(constants.BACKGROUND_COLOR)
                for i, it in mapp:
                    if it != 0:
                        screen.blit(it.img, (it.x * TILE_SIZE, it.y * TILE_SIZE))
                screen.blit(hero.img, (hero.x * TILE_SIZE, hero.y * TILE_SIZE))
                screen.blit(inventory_surf, (MAP_W,0))
                draw_UI(screen, hero, in_inventory_mode)
                pygame.display.update()



if __name__ == "__main__":
    main()