import argparse
import os
import random
import time
import numpy as np


class PetriDish:
    EMPTY = 0
    CELL = 1

    def __init__(self, grid_size=32, cells=205):
        """make a n x n petri dish and place cells

        Generates a n x n 2D numpy array and randomly places a number of cells into that numpy array.
        :param grid_size: size of n to generate an n x n
        :param cells: number of cells to place
        """
        self.grid_size = grid_size
        self.cells = cells
        self.grid = np.zeros((grid_size, grid_size), dtype=np.uint8)
        self.__init_grid()

    def __init_grid(self):
        """Place cells into the grid randomly until the specified number of cells is placed"""
        placed_cells = 0
        while placed_cells < self.cells:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.grid[x, y] == PetriDish.EMPTY:  # don't place cells if a cell is already present
                self.grid[x, y] = PetriDish.CELL
                placed_cells += 1  # make sure not to forget to increment the loop condition or this runs infinitely

    def __repr__(self):
        """Generate string out of the petri dish by making evey cell a '0' and every empty space a ' '"""
        representation = ''
        # we are drawing x as the vertical axis and y as the horizontal axis,
        # maybe unintuitive but effectively arbitrary
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                representation += '0' if self.grid[x, y] == PetriDish.CELL else ' '
            representation += '\n'
        return representation

    def update(self):
        """simulate a generation of cell growth

        Cells with 2 or 3 neighbors survive. 3 neighbors cells procreate to the current cell.
        """
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # sum the number of cell neighbors starting from (x - 1, y - 1) to (x + 1, y + 1)
                neighbors = self.grid[(x - 1) % self.grid_size, (y - 1) % self.grid_size] + \
                            self.grid[(x - 1) % self.grid_size, y] + \
                            self.grid[(x - 1) % self.grid_size, (y + 1) % self.grid_size] + \
                            self.grid[x, (y - 1) % self.grid_size] + \
                            self.grid[x, (y + 1) % self.grid_size] + \
                            self.grid[(x + 1) % self.grid_size, (y - 1) % self.grid_size] + \
                            self.grid[(x + 1) % self.grid_size, y] + \
                            self.grid[(x + 1) % self.grid_size, (y + 1) % self.grid_size]

                # cells that don't have either 2 or 3 neighbors die either from under- or overpopulation
                if self.grid[x, y] == PetriDish.CELL and (neighbors < 2 or neighbors > 3):
                    self.grid[x, y] = PetriDish.EMPTY
                # 3 neighbor cells procreate to create a new cell
                elif self.grid[x, y] == PetriDish.EMPTY and neighbors == 3:
                    self.grid[x, y] = PetriDish.CELL


def clear():
    # windows compatibility
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def main(args):
    dish = PetriDish(args.grid, args.cells)
    for i in range(args.generations):
        if args.clear:
            clear()
        print("Generation {} -------------------".format(i + 1))
        dish.update()
        print(dish)
        time.sleep(args.interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # default 32 x 32 grid
    parser.add_argument('--grid', type=int, help='size of the n x n grid', default=32)
    # default 20% cells alive
    parser.add_argument('--cells', type=int, help='number of live cells to place', default=205)
    parser.add_argument('--generations', type=int, help='number of generations', default=10)
    # makes commandline runs pretty
    parser.add_argument('--clear', action='store_true', help='clear shell between each generation', default=False)
    # you can kind of decide on FPS using this option, default is 1 FPS
    parser.add_argument('--interval', type=float, help='time in seconds between generation', default=1)
    main(parser.parse_args())
