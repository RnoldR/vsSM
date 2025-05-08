# Code initialisatie: logging
import logging
logger = logging.getLogger()

import os
import time
import yaml
import pygame
import random
import numpy as np
import pandas as pd

from math import sqrt

from grid import Grid

from grid_thing_data import COL_NAME, COL_DESCRIPTION, COL_CATEGORY, \
    COL_CHAR, COL_DATA, COL_ICON, COL_COLOR

# forward declaration
class Thing: pass
class Grid: pass

class Thing():
    # Define static sequence number to have unique ID's
    Seq: int = 0
    Verbose: int = 1
    definitions: pd.DataFrame
    
    def __init__(self, location: tuple, grid: Grid):
        # increment sequence number
        Thing.Seq += 1

        # system attributes
        self.id: int = Thing.Seq
        self.location: tuple = location
        self.row, self.col = self.location
        self.grid: object = grid
        self.deleted: bool = False

        # assign the name from the class itself as it is created
        # use this name to fetch its attributes from the definitions table
        self.type: str = self.get_type() # __class__.__name__
        self.name: str = f'{self.__class__.__name__}'
        self.description: str = '' 
        self.category: int = ''
        self.char: str =''
        self.data: str = ''
        self.icons: object = ''
        
        # some general attributes
        self.visible: bool = True
        self.ticks: int = 0
        
        self.sensors = []
        self.effectors = []

        return
    
    ### __init__ ###

    @staticmethod
    def set_definitions(res_path: str, style: int):
        
        config_file = os.path.join(res_path, 'config', 'things.csv')
        definitions = pd.read_csv(
            config_file, 
            sep = ';', 
            index_col = COL_NAME,
        )

        # Add columns for Icon and Color
        definitions[COL_ICON] = None
        definitions[COL_COLOR] = None

        # next load icon info from images is resource path
        for key in definitions.index:
            filename = key.lower() + '-' + str(style) + '.png'
            filename = os.path.join('images', filename)
            filename = os.path.join(res_path, filename)
            
            definitions.loc[key, 'Icon'] = pygame.image.load(filename)

            # Extract color from icon
            # img = definitions.loc[key, COL_ICON].copy()

        # for

        Thing.definitions = definitions

        return
    
    ### set_definitions ###
    
    def d(self, loc) -> float:
        if self.location != None:
            dx = self.location[0] - loc[0]
            dy = self.location[1] - loc[1]
            
            dd = dx * dx + dy * dy
            
            if dd > 0:
                return sqrt(dd)
            else:
                return 0
        else:
            return -1
        
    ### d ###

    def get_type(self) -> str:

        return self.__class__.__name__

    ### get_type ###
    
    def cost(self, grid, direction):
        ''' Computes the cost of a turn.
        
        Args:
            grid (np.arry): grid on which to perform the move
            direction (char): direction in which to move
            
        Returns:
            The cost of the move when it should be effected (float)
        '''

        return -1, True
    
    ### cost ###
    
    def next_turn(self):
        # thing ages a unit
        self.ticks += 1

        return
    ### next_turn ###
    
    def move(self, grid, direction=None):
        
        return
    
    ### move ###
    
### Class: Thing ###
