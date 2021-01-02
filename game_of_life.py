import argparse
import math
import pygame
from petri_dish import PetriDish

SIZE = 10
TARGET_FPS = 30
COLOR = (0, 255, 0)  # Green


def handle_mouse_held(dish, surface, screen):
    """place living cells in the grid below the mouse while mouse button is held down

    Draw living cells onto the grid while the mouse button is held down. This will interrupt the main game loop until
    the mouse button is released.
    """
    mouse_held_down = True
    while mouse_held_down:
        # find position of mouse on the grid
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = math.floor(mouse_x / SIZE)
        grid_y = math.floor(mouse_y / SIZE)
        dish.grid[grid_x, grid_y] = PetriDish.CELL

        # redraw the game screen with the new cell
        surface.fill((0, 0, 0))
        draw_petri_dish(dish, surface)
        screen.blit(surface, (0, 0))
        pygame.display.flip()

        # exit out of loop when the mouse button is released
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held_down = False


def draw_petri_dish(dish, surface):
    """draw rectangles onto the surface for each living cell in the dish"""
    for x in range(dish.grid_size):
        for y in range(dish.grid_size):
            if dish.grid[x, y] == PetriDish.CELL:
                pygame.draw.rect(surface, COLOR, (x * SIZE, y * SIZE, SIZE, SIZE))


def main(args):
    pygame.init()
    # window size is determined mainly by grid size
    window_size = args.grid * SIZE
    screen = pygame.display.set_mode((window_size, window_size))

    # initialize main drawing surface
    surface = pygame.Surface(screen.get_size())
    surface.fill((0, 0, 0))

    clock = pygame.time.Clock()
    # updates to the state are time-based and separate from the FPS
    update_interval = int(args.interval * 1000)  # convert to milliseconds
    last_update = pygame.time.get_ticks()

    # initialize the actual simulation model
    dish = PetriDish(args.grid, args.cells)

    # main game loop
    run = True
    while run:
        clock.tick(TARGET_FPS)
        current_ticks = pygame.time.get_ticks()
        # initial draw, current_ticks can only be under update_interval once at
        # the beginning (not accounting for overflow)
        if current_ticks < update_interval:
            draw_petri_dish(dish, surface)
        # updates
        if (current_ticks - last_update) > update_interval:
            last_update = current_ticks
            dish.update()
            # redraw
            surface.fill((0, 0, 0))
            draw_petri_dish(dish, surface)
        # set screen state to state of drawing surface
        screen.blit(surface, (0, 0))
        pygame.display.flip()

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_held(dish, surface, screen)

    pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--grid', type=int, help='size of the n x n grid', default=32)
    parser.add_argument('--cells', type=int, help='number of live cells to place', default=100)
    parser.add_argument('--interval', type=float, help='time in seconds between generation', default=0.5)
    main(parser.parse_args())
