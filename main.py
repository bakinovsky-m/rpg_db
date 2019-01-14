import pygame
import pypika
from pypika import Order

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

def create_monsters_list(db):
    t = pypika.Table('monsters')
    q = pypika.Query.from_(t).select('*').get_sql()
    monster_res = db.select(q)
    monsters = []
    # id name lvl base_health base_damage curr_location item asset
    for mr in monster_res:
        t = pypika.Table('items')
        q = pypika.Query.from_(t).select('*').where(t.id == mr[6]).get_sql()
        rrr = db.select(q)[0]
        rarity = mr[8]
        monst_count = (1/rarity) * (MAP_W / TILE_SIZE) * (MAP_H / TILE_SIZE) / 5
        monst_count = round(monst_count)
        for _ in range(monst_count):
            item_to_monst = Item(rrr[0], rrr[1], make_pygame_image(rrr[5]), rrr[2], rrr[4], rrr[3])
            monsters.append(Monster(mr[0], mr[1], mr[3], mr[4], item_to_monst, 0, 0, make_pygame_image(mr[7]), mr[8], mr[9]))
    return monsters

def change_location(char, mmap, dx, dy, db):
    cur_x = char.curr_location.x
    cur_y = char.curr_location.y

    for l in LOCATIONS:
        if l.x == (cur_x + dx) and l.y == (cur_y + dy):
            global CUR_LOCATION
            CUR_LOCATION = l
            char.curr_location = l
            constants.BACKGROUND_COLOR = char.curr_location.rgb
            if dx > 0:
                char.x = 0
            elif dx < 0:
                char.x = mmap.w - 1
            if dy > 0:
                char.y = 0
            elif dy < 0:
                char.y = mmap.h - 1

            t = pypika.Table('characters')
            q = pypika.Query.update(t).set(t.curr_location, l.id).where(t.id == char.id).get_sql()
            db.update(q)

            mmap.random_fill(create_monsters_list(db))
            return True

    return False

def leveling(char, exp, db):
    t = pypika.Table('lvl_exp')
    q = pypika.Query.from_(t).select('*').get_sql()
    res = db.select(q)

    char.exp += exp
    for r in res:
        if r[0] == char.lvl + 1 and r[1] <= char.exp:
            char.lvl += 1
            char.recalculate_basics()
            # t = pypika.
    t = pypika.Table('characters')
    q = pypika.Query.update(t).set(t.lvl, char.lvl).set(t.curr_exp, char.exp).where(t.id == char.id).get_sql()
    db.update(q)

def move(char, mmap, dx, dy, db):
    if not mmap.is_ok_move(char, dx, dy):
        change_location(char, mmap, dx, dy, db)
        return
    index = (char.x + dx) + (char.y + dy)*mmap.w
    mmmap = mmap.cells[index]
    if isinstance(mmmap, Monster):
        monst = mmmap

        monst.health -= char.get_attack()
        if monst.health <= 0:
            mmap.cells[index] = monst.item
            monst.item.x = monst.x
            monst.item.y = monst.y
            leveling(char, monst.exp, db)
        else:
            char.curr_health -= monst.base_dmg - char.inventory.get_block()

            # death
            if char.curr_health <= 0:
                q = '''DELETE FROM characters WHERE id=''' + str(char.id)
                db.insert(q)
                q = '''DELETE FROM items_in_inventory WHERE inv=''' + str(char.inventory.id)
                db.insert(q)
                q = '''DELETE FROM inventories WHERE id=''' + str(char.inventory.id)
                db.insert(q)
    else:
        char.x += dx
        char.y += dy

def draw_UI(screen, hero, in_inventory_mode):
    f = pygame.font.SysFont('Noto Mono', TEXT_SIZE)

    INFO_BAR = []

    INFO_BAR.append(f.render(hero.name + ", " + hero.curr_location.name, False, TEXT_COLOR))
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
        if in_inventory_mode and cur_item == CUR_ITEM:
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

def start_menu(db):
    print('1. Choose existing character')
    print('2. Create new character')
    print('3. List existing characters')
    print('You always can input 0 to return to main menu')
    available_anses = [1,2,3]
    ans = input('> ')
    try:
        ans = int(ans)
        if ans not in available_anses:
            return -1
    except ValueError:
        return -1

    if ans == 0:
        return -1
    if ans == 1:
        t = pypika.Table('characters')
        q = pypika.Query.from_(t).select('*').get_sql()
        res = db.select(q)

        print()
        for r in res:
            print(r[1] + ', lvl ' + str(r[2]))
        print()
        hero_name = input('hero name: ')
        if hero_name == '0':
            return -1
        t = pypika.Table('characters')
        q = pypika.Query.from_(t).select('*').where(t.name == hero_name).get_sql()
        hero_res = db.select(q)
        try:
            hero_res = hero_res[0]
        except IndexError:
            print('no such character')
            return -1
        print('starting your adventure')
        return hero_res
    if ans == 2:
        print()
        name = input('Name: ')
        if name == '0':
            return -1
        print('Available classes: ')
        t = pypika.Table('classes')
        q = pypika.Query.from_(t).select('*').get_sql()
        class_res = db.select(q)
        i = 0
        for r in class_res:
            print(str(i+1) + '.', r[1] + " (hp: " + str(r[2]) + ", dmg: " + str(r[3]) + ')')
            i += 1
        class_ = input('No. of class: ')
        if class_ == '0':
            return -1
        class_ = int(class_)
        class_ -= 1 # for right indexation

        t = pypika.Table('inventories')
        q = pypika.Query.into('inventories').columns(t.capacity).insert(3).get_sql()
        db.insert(q)

        q = pypika.Query.from_(t).select('id').orderby('id', order=Order.desc).get_sql()
        new_inv = db.select(q)[0]

        t = pypika.Table('characters')
        q = pypika.Query.into(t).columns(
                t.name,
                t.base_health,
                t.base_damage,
                t.curr_location,
                t.inventory,
                t.class_
            ).insert(
                name,
                class_res[class_][2],
                class_res[class_][3],
                1,
                new_inv[0],
                class_res[class_][0]
            ).get_sql()
        db.insert(q)

        q = pypika.Query.from_(t).select("*").where(t.name == name).get_sql()
        res = db.select(q)[0]
        print('new character have been created')
        return res

    if ans == 3:
        t = pypika.Table('characters')
        q = pypika.Query.from_(t).select('*').get_sql()
        res = db.select(q)

        print()
        for r in res:
            print(r[1] + ', lvl ' + str(r[2]))
        print()
        return -1

def main():
    # INIT
    db = DBHandler()

    # id name lvl curr_exp base_health base_damage curr_location inventory 
    hero_res = start_menu(db)

    while hero_res == -1:
        hero_res = start_menu(db)

    # INVENTORY
    t = pypika.Table('inventories')
    q = pypika.Query.from_(t).select('*').where(t.id == hero_res[7]).get_sql()
    # id capacity size
    inv_res = db.select(q)[0]
    heros_inv = Inventory(inv_res[0], inv_res[1], inv_res[2], db)

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
    mapp.random_fill(create_monsters_list(db))

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
    while running and hero.curr_health > 0:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                    break
                if e.key == pygame.K_i:
                    in_inventory_mode = not in_inventory_mode

                if not in_inventory_mode:
                    if e.key == pygame.K_UP:
                        move(hero, mapp, 0, -1, db)
                    if e.key == pygame.K_DOWN:
                        move(hero, mapp, 0, 1, db)
                    if e.key == pygame.K_LEFT:
                        move(hero, mapp, -1, 0, db)
                    if e.key == pygame.K_RIGHT:
                        move(hero, mapp, 1, 0, db)

                    if hero.curr_health <= 0:
                        break
                    hero.regenerate()

                else:
                    global CUR_ITEM
                    if e.key == pygame.K_UP:
                        if CUR_ITEM != 0:
                            CUR_ITEM -= 1
                    if e.key == pygame.K_DOWN:
                        if CUR_ITEM < hero.inventory.size - 1:
                            CUR_ITEM += 1
                    if e.key == pygame.K_g:
                        index = hero.x + hero.y*mapp.w
                        mmmap = mapp.cells[index]
                        if isinstance(mmmap, Item):
                            if hero.take_item(mmmap):
                                mapp.cells[index] = 0
                    if e.key == pygame.K_d:
                        hero.drop_item(hero.inventory.items[CUR_ITEM])

                screen.fill(constants.BACKGROUND_COLOR)
                for i, it in mapp:
                    if it != 0:
                        screen.blit(it.img, (it.x * TILE_SIZE, it.y * TILE_SIZE))
                        if isinstance(it, Monster):
                            health_bar = pygame.Surface((TILE_SIZE * (it.health / it.base_health), int(TILE_SIZE/10)))
                            health_bar.fill(hex_to_rgb('#00FF00'))
                            screen.blit(health_bar, (it.x * TILE_SIZE, (it.y * TILE_SIZE)))

                health_bar = pygame.Surface((TILE_SIZE * (hero.curr_health / hero.get_total_health()), int(TILE_SIZE/10)))
                health_bar.fill(hex_to_rgb('#00FF00'))
                screen.blit(health_bar, (hero.x * TILE_SIZE, (hero.y *TILE_SIZE) - 10))
                screen.blit(hero.img, (hero.x * TILE_SIZE, hero.y * TILE_SIZE))

                screen.blit(inventory_surf, (MAP_W,0))
                draw_UI(screen, hero, in_inventory_mode)
                pygame.display.update()
    if hero.curr_health <= 0:
        print('Your character is totally dead :(')
        print('Make another one and good luck!')



if __name__ == "__main__":
    main()