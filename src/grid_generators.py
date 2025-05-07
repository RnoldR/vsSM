# import logging
from create_logger import create_logger
logger = create_logger.create_log('grid-vehicles.log')

import os
import time
import pygame
import random
import numpy as np
import pandas as pd

from grid_objects import Person
from grid_viewer import GridViewObject
from grid import Grid, GridMatrix, GridObjects

# from grid_thing_data import COL_NAME, COL_DESCRIPTION, COL_CATEGORY, \
#     COL_CHAR, COL_DATA, COL_ICON

# Initialize Pandas  display options such that the whole DataFrame is printed
pd.options.display.max_rows = 999999
pd.options.display.max_columns = 999999


class GridGenerator(object):
    def __init__(self):
        return
    
    def generate(self):

        return 
    
### GridGenerator ###


class GridMatrixGenerator(GridGenerator):
    def __init__(self):

        return

    ### init ###
    

    def generate(
            self,
            grid_size = (8,12), 
            res_path: str = '', 
            icon_style: int = 1,
            verbose: int = 1,
            generator_function = None
        ):

        grid = GridMatrix(grid_size, res_path, icon_style)
        grid.set_verbose(verbose)

        for row in range(grid.rows):
            for col in range(grid.cols):
                thing = generator_function((row, col), grid)
                grid.insert_thing(thing, (row, col))
        
        return grid

    ### generate ###

### Class: GridMatrixGenerator ###


class GribObjectGenerator(GridGenerator):

    def __init__(self):
        return
    

    def generate(
            self,
            grid_size = (8,12), 
            res_path: str = '', 
            icon_style: int = 1,
            verbose: int = 1
        ):

        grid = GridObjects(grid_size, res_path, icon_style)
        grid.set_verbose(verbose)
        
        return grid

    ### generate ###


    def generate_fixed(
            self,
            grid_size = (8,12), 
            res_path: str = '', 
            icon_style: int = 1,
            verbose: int = 1
        ):
            
        grid = GridObjects(grid_size, res_path, icon_style)
        grid.set_verbose(verbose)

        return grid
    
    # generate #    
    
### Class: GribObjectGenerator ###
