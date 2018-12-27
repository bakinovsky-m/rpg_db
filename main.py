import pygame
import pypika

from character import Character
from monster import Monster
from inventory import Inventory
from db_handler import DBHandler
from item import Item
from map import Map

DISPLAY_W = 700
DISPLAY_H = 400
FPS = 30

def move(char, mmap, dx, dy):
    if (char.x + dx) < 0 or (char.x + dx) > DISPLAY_W:
        dx = 0
    if (char.y + dy) < 0 or (char.y + dy) > DISPLAY_H:
        dy = 0
    mmmap = mmap.cells[(char.x + dx) + (char.y + dy)*DISPLAY_W]
    if mmmap != 0:
        # print('QWEQWE')
        if isinstance(mmmap, Monster):
            monst = mmmap
            print('char health', char.health)
            print('monst health', monst.health)
            char.health -= monst.base_dmg - char.inventory.get_block()
            monst.health -= char.get_attack()
            if monst.health <= 0:
                mmap.cells[(char.x + dx) + (char.y + dy)*DISPLAY_W] = monst.item
        elif isinstance(mmmap, Item):
            if char.take_item(mmmap):
                mmap.cells[(char.x + dx) + (char.y + dy)*DISPLAY_W] = 0
            char.x += dx
            char.y += dy
    else:
        char.x += dx
        char.y += dy



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

    t = pypika.Table('inventories')
    q = pypika.Query.from_(t).select('*').where(t.id == hero_res[7]).get_sql()
    # id capacity size
    inv_res = db.select(q)[0]
    heros_inv = Inventory(inv_res[0], inv_res[1], inv_res[2], db)

    t = pypika.Table('monsters')
    q = pypika.Query.from_(t).select('*').get_sql()
    monster_res = db.select(q)
    monsters = []
    # id name lvl base_health base_damage curr_location item asset
    for mr in monster_res:
        t = pypika.Table('items')
        q = pypika.Query.from_(t).select('*').where(t.id == mr[6]).get_sql()
        rrr = db.select(q)[0]
        item_to_monst = Item(rrr[0], rrr[1], rrr[5], rrr[2], rrr[4], rrr[3])
        monsters.append(Monster(mr[0], mr[1], mr[3], mr[4], item_to_monst, 0, 0, pygame.image.load(mr[7])))

    # PYGAME
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([DISPLAY_W, DISPLAY_H])

    mapp = Map(DISPLAY_W, DISPLAY_H)
    mapp.random_fill(monsters)

    hero = Character(hero_res[0], hero_name, hero_res[4], hero_res[5], heros_inv, 10, 10, pygame.image.load("assets/hero.png"))

    running = True

    while running:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False

                if e.key == pygame.K_UP:
                    move(hero, mapp, 0, -10)
                if e.key == pygame.K_DOWN:
                    move(hero, mapp, 0, 10)
                if e.key == pygame.K_LEFT:
                    move(hero, mapp, -10, 0)
                if e.key == pygame.K_RIGHT:
                    move(hero, mapp, 10, 0)

                screen.fill((0, 0, 0))
                for i, it in mapp:
                    if it != 0:
                        # print('monst', it.x, it.y)
                        screen.blit(it.img, (i % DISPLAY_W, i // DISPLAY_W))
                screen.blit(hero.img, (hero.x, hero.y))
                # print('hero', hero.x, hero.y)
                pygame.display.update()



if __name__ == "__main__":
    main()