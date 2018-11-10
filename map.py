import pygame

from item import Item

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h

        self.cells = []

        for _ in range(w + h):
            self.cells.append(Item('none'))

        self.__random_fill()

    def __random_fill(self):
        self.cells[901] = Item('sword', 1, 0, pygame.image.load('assets/sword.png'))

    def print(self):
        for i in range(self.w):
            for j in range(self.h):
                print(0, end='')
            print()

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        self.n += 1
        if self.n >= len(self.cells):
            raise StopIteration
        return self.n, self.cells[self.n]