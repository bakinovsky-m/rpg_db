import random

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h

        self.cells = []

        for _ in range(w * h):
            self.cells.append(0)

    def random_fill(self, monsters):
        for m in monsters:
            rand_w = (random.randint(0, self.w) // 10) * 10
            rand_h = (random.randint(0, self.h) // 10) * 10
            while self.cells[rand_h * self.w + rand_w] != 0:
                rand_w = (random.randint(0, self.w) // 10) * 10
                rand_h = (random.randint(0, self.h) // 10) * 10
            self.cells[rand_h * self.w + rand_w] = m
            m.x = rand_w
            m.y = rand_h

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