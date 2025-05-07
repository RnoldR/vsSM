# import logging
from create_logger import create_logger
logger = create_logger.create_log('grid-vehicles.log')

import os
import time
import yaml
import pygame
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from grid_viewer import GridViewMatrix
from grid_generators import GridMatrixGenerator
from grid_thing import Thing
from grid_objects import Person

# Initialize Pandas  display options such that the whole DataFrame is printed
pd.options.display.max_rows = 999999
pd.options.display.max_columns = 999999


class InfectiousDiseaseModel(object):
    def __init__(self, res_path: str):

        # read config file and assign to instance variables
        with open(os.path.join(res_path, 'config', 'config.yaml')) as infile:
            config = yaml.safe_load(infile)

        self.res_path = res_path
        self.screen_width = config['screen_width']
        self.screen_height = config['screen_height']
        self.rows = config['rows']
        self.cols = config['cols']
        self.icon_style = config['icon_style']
        self.epochs = config['epochs']
        self.states = config['states']

        # read Thing definition file
        Thing.set_definitions(res_path, self.icon_style)

        # create directory to save results to
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S").replace(' ', '_')
        self.result_dir = os.path.join(res_path, 'results', now)
        os.mkdir(self.result_dir)
        print('Results will be written to', self.result_dir)

        return
    
    ### __init__###


    def generator_function(self, location: tuple, grid: object):

        person = Person(location, grid)

        for state, locations in self.states.items():
            if locations == '*':
                person.set_state(state)
            else:
                if location in locations:
                    person.set_state(state)
            # if

        
        # for

        return person

    ### generator_function ###


    def initial_seed(self, grid: object, state: str):
        mid_row = int(self.rows / 2)
        mid_col = int(self.cols / 2)
        seed = [(mid_row, mid_col)]

        for location in seed:
            grid.matrix[location].set_state(state)        

        return
    
    ### initial_seed ###


    def run_simple_epidemic(self):

        # Create a grid generator
        generator = GridMatrixGenerator()

        # create a grid with appropriate number of columns and rows
        grid = generator.generate(
            grid_size = (self.rows, self.cols), 
            res_path = self.res_path, 
            icon_style = self.icon_style,
            generator_function = self.generator_function,
        )
        self.initial_seed(grid, 'Y')

        grid.create_recorder(Thing.definitions, self.epochs)
    
        # define a grid viewer for the grid
        grid_viewer = GridViewMatrix(
            grid = grid, 
            definitions = Thing.definitions, 
            screen_size = (self.screen_width, self.screen_height),
        )
        
        grid_viewer.update_screen()

        while grid.ticks <= self.epochs:
            # print(f'Turn: {grid.ticks}')
            if grid.ticks % 100 == 0:
                save_file = os.path.join(self.result_dir, f'model_run_{grid.ticks}.png')
                pygame.image.save(grid_viewer.grid_layer, save_file)

            grid_viewer.update_screen()
            grid.next_turn()

        # while

        grid.recorder.to_csv(os.path.join(self.result_dir, 'model_output.csv'), sep=';')
        
        self.plot(grid.recorder)

        # input('Press <enter> to quit')
        pygame.quit()
        
        return
        
    ### test_move_around ###


    def plot(self, df: pd.DataFrame):  
        plt.figure()
        df.plot()
        plt.xlabel('t (days)')
        plt.ylabel('Numbere of persons')
        plt.title('Infectious Disease Model Run')
        plt.legend(loc='best')
        plt.savefig(os.path.join(self.result_dir, 'model_plot.png'))
        plt.show()

        return
    
    ### plot ###

### Class: InfectiousDiseaseModel ###

