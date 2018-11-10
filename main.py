import pygame

from character import Character
from inventory import Inventory
from item import Item
from map import Map

DISPLAY_W = 800
DISPLAY_H = 600
FPS = 30

def move(char, dx, dy):
    if (char.x + dx) <= 0 or (char.x + dx) >= DISPLAY_W:
        dx = 0
    if (char.y + dy) <= 0 or (char.y + dy) >= DISPLAY_H:
        dy = 0
    char.x += dx
    char.y += dy


def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode([DISPLAY_W, DISPLAY_H])

    mapp = Map(DISPLAY_W, DISPLAY_H)

    mans_inv = Inventory()
    hero = Character('hero', mans_inv, 101, 101, pygame.image.load("assets/hero.png"))

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
                    move(hero, 0, -10)
                if e.key == pygame.K_DOWN:
                    move(hero, 0, 10)
                if e.key == pygame.K_LEFT:
                    move(hero, -10, 0)
                if e.key == pygame.K_RIGHT:
                    move(hero, 10, 0)

        screen.fill((0, 0, 0))
        for i, it in mapp:
            if it.name != 'none':
                screen.blit(it.img, (i // DISPLAY_W, i % DISPLAY_W))
        screen.blit(hero.img, (hero.x, hero.y))
        pygame.display.update()



if __name__ == "__main__":
    main()