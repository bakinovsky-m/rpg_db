import random
import math

from constants import TILE_SIZE

class Map:
    def __init__(self, w, h):
        self.w = math.floor((w / TILE_SIZE))
        self.h = math.floor((h / TILE_SIZE))

        self.cells = []

        for _ in range(self.w * self.h):
            self.cells.append(0)

    def random_fill(self, monsters):
        for n, c in enumerate(self.cells):
            self.cells[n] = 0
        for m in monsters:
            rand_x = random.randint(0, self.w - 1)
            rand_y = random.randint(0, self.h - 1)
            while self.cells[rand_y * self.w + rand_x] != 0:
                rand_x = random.randint(0, self.w - 1)
                rand_y = random.randint(0, self.h - 1)
            self.cells[rand_y * self.w + rand_x] = m
            m.x = rand_x
            m.y = rand_y

    def is_ok_move(self, char, dx, dy):
        if ((char.x + dx) < 0) or ((char.x + dx) >= self.w):
            return False
        if ((char.y + dy) < 0) or ((char.y + dy) >= self.h):
            return False
        return True

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
        return self.n - 1, self.cells[self.n - 1]