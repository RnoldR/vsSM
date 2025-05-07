# import logging
from telnetlib import GA
from create_logger import create_logger
logger = create_logger.create_log('grid-vehicles.log')

import os
import time
import pygame
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from grid_viewer import GridViewMatrix
from grid import Grid, GridMatrix
from grid_generators import GridMatrixGenerator
from grid_thing import Thing
from grid_objects import Person

from grid_thing_data import COL_NAME, COL_DESCRIPTION, COL_CATEGORY, \
    COL_CHAR, COL_DATA, COL_ICON

# Initialize Pandas  display options such that the whole DataFrame is printed
pd.options.display.max_rows = 999999
pd.options.display.max_columns = 999999

# Constants
EPOCHS = 10
STATES = {'X': '*'}

def generator_function(location: tuple, grid: Grid):

    mid_row = int(grid.rows / 2)
    mid_col = int(grid.cols / 2)
    seed = [(mid_row, mid_col)]
    person = Person(location, grid)

    for state, locations in STATES.items():
        if location in seed:
            person.set_state('Y')
        elif locations == '*':
            person.set_state(state)
        else:
            if location in locations:
                person.set_state(state)
        # if

    
    # for

    return person

### generator_function ###


def test_simple_infection(res_path: str, icon_style: int):
    screen_width = 1000
    screen_height = 1000
    rows = 10
    cols = 10

    # Create a grid generator
    generator = GridMatrixGenerator()

    # create a grid with appropriate number of columns and rows
    grid = generator.generate(
        grid_size = (rows, cols), 
        res_path = res_path, 
        icon_style = icon_style,
        generator_function = generator_function,
    )
    grid.create_recorder(Thing.definitions, EPOCHS)

    # define a grid viewer for the grid
    grid_viewer = GridViewMatrix(
        grid = grid, 
        definitions = Thing.definitions, 
        screen_size = (screen_width, screen_height),
    )
    
    logger.info(grid.print_grid(grid.matrix))

    grid_viewer.update_screen()
    # time.sleep(1)
    print(grid.recorder)

    while grid.ticks <= EPOCHS:
        print(f'Turn: {grid.ticks}')

        grid_viewer.update_screen()
        grid.next_turn()

    # while
    
    print(grid.recorder)
    input('Press <enter> to quit')
    pygame.quit()
    
    return
    
### test_move_around ###


if __name__ == "__main__":
    random.seed(42)

    res_path = '/media/i-files/home/arnold/development/python/vsSM'
    Thing.set_definitions(res_path, 1)

    test_simple_infection(res_path, 1)
   