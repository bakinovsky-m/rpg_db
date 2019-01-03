import time

import pygame
import pypika

from character import Character
from monster import Monster
from inventory import Inventory
from db_handler import DBHandler
from item import Item
from map import Map

from constants import DISPLAY_H, DISPLAY_W, BACKGROUND_COLOR, TILE_SIZE, FPS

def move(char, mmap, dx, dy):
    if not mmap.is_ok_move(char, dx, dy):
        print('no way')
        return
    # mmmap = mmap.cells[(char.x + dx) + (char.y + dy)*DISPLAY_W]
    index = (char.x + dx) + (char.y + dy)*mmap.w
    # mmmap = mmap.cells[(char.x + dx) + (char.y + dy)*mmap.w]
    mmmap = mmap.cells[index]
    if mmmap != 0:
        if isinstance(mmmap, Monster):
            monst = mmmap
            print('before fight')
            print('char health', char.health)
            print('monst health', monst.health)
            char.health -= monst.base_dmg - char.inventory.get_block()
            monst.health -= char.get_attack()
            if monst.health <= 0:
                # mmap.cells[(char.x + dx) + (char.y + dy)*mmap.w] = monst.item
                mmap.cells[index] = monst.item
                monst.item.x = monst.x
                monst.item.y = monst.y
            print('after fight')
            print('char health', char.health)
            print('monst health', monst.health)
        elif isinstance(mmmap, Item):
            if char.take_item(mmmap):
                mmmap.x = -1
                mmmap.y = -1
                # mmap.cells[(char.x + dx) + (char.y + dy)*mmap.w] = 0
                mmap.cells[index] = 0
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
        # item_to_monst = Item(rrr[0], rrr[1], rrr[5], rrr[2], rrr[4], rrr[3])
        item_to_monst = Item(rrr[0], rrr[1], 'assets/dagger.png', rrr[2], rrr[4], rrr[3])
        # monsters.append(Monster(mr[0], mr[1], mr[3], mr[4], item_to_monst, 0, 0, pygame.image.load(mr[7])))
        monsters.append(Monster(mr[0], mr[1], mr[3], mr[4], item_to_monst, 0, 0, pygame.image.load('assets/rat.png')))

    # PYGAME
    pygame.init()
    # pygame.font.init()
    pygame.key.set_repeat(300, 300)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([DISPLAY_W, DISPLAY_H], pygame.DOUBLEBUF)

    mapp = Map(DISPLAY_W, DISPLAY_H)
    mapp.random_fill(monsters, 2)

    hero = Character(hero_res[0], hero_name, hero_res[4], hero_res[5], heros_inv, 0, 0, pygame.image.load("assets/new_hero.png"))

    # myfont = pygame.font.SysFont('Noto Mono', 30)
    # ui_surface = myfont.render('asd', False, (255,0,0))

    start = time.time()
    screen.fill(BACKGROUND_COLOR)
    # start = time.time()
    for i, it in mapp:
        if it != 0:
            screen.blit(it.img, (it.x * TILE_SIZE, it.y * TILE_SIZE))
    # print('start:', time.time() - start)
    screen.blit(hero.img, (hero.x * TILE_SIZE, hero.y * TILE_SIZE))
    # screen.blit(ui_surface, (0,0))
    pygame.display.update()
    print('start:', time.time() - start)

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
                if e.key == pygame.K_q:
                    print(hero.x, hero.y)
                    break

                if e.key == pygame.K_UP:
                    move(hero, mapp, 0, -1)
                if e.key == pygame.K_DOWN:
                    move(hero, mapp, 0, 1)
                if e.key == pygame.K_LEFT:
                    move(hero, mapp, -1, 0)
                if e.key == pygame.K_RIGHT:
                    move(hero, mapp, 1, 0)

                screen.fill(BACKGROUND_COLOR)
                # start = time.time()
                for i, it in mapp:
                    if it != 0:
                        screen.blit(it.img, (it.x * TILE_SIZE, it.y * TILE_SIZE))
                # print('start:', time.time() - start)
                screen.blit(hero.img, (hero.x * TILE_SIZE, hero.y * TILE_SIZE))
                # screen.blit(ui_surface, (0,0))
                pygame.display.update()



if __name__ == "__main__":
    main()