# import logging
from create_logger import create_logger
logger = create_logger.create_log('grid-vehicles.log')

import os
import time
import yaml
import pygame
import pandas as pd
import matplotlib.pyplot as plt
import moviepy.video.io.ImageSequenceClip

from datetime import datetime

from grid_viewer import GridViewMatrix
from grid_generators import GridMatrixGenerator
from grid_thing import Thing
from grid_objects import Person

from grid_thing_data import COL_NAME, COL_DESCRIPTION, COL_CATEGORY, \
    COL_CHAR, COL_DATA, COL_ICON, COL_COLOR


class InfectiousDiseaseModel(object):
    def __init__(self, res_path: str):

        # read config file and assign to instance variables
        with open(os.path.join(res_path, 'config', 'config.yaml')) as infile:
            config = yaml.safe_load(infile)

        self.config_screen = config['Screen']
        self.config_pop = config['Population']
        self.config_model = config['Infectionmodel']

        self.res_path = res_path
        self.screen_width = self.config_screen['screen_width']
        self.screen_height = self.config_screen['screen_height']
        self.rows = self.config_screen['rows']
        self.cols = self.config_screen['cols']
        self.icon_style = self.config_screen['icon_style']
        self.epochs = self.config_screen['epochs']

        self.initializations = self.config_model['initialization']
        # self.states = self.config_model['states']

        # read Thing definition file
        Thing.set_definitions(res_path, self.icon_style)  

        # create directory to save results to
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S").replace(' ', '_')
        self.result_dir = os.path.join(res_path, 'results', now)
        os.makedirs(os.path.join(self.result_dir, 'images'))
        print('Results will be written to', self.result_dir)

        return
    
    ### __init__###


    @staticmethod
    def recurrent_p(p: float, n: int) -> float:
        """ Returns recurrent probability.

        Args:
            q (float): recurrent probability
            n (int): number of occurrences

        Returns:
            float: single probability
        """

        return (1 - (1 - p) ** (1 / n))

    ### recurrent_p ###
    @staticmethod
    def inverse_p(p: float, n: int) -> float:
        """ Computes the inverse of recurrent probability.

        Args:
            p (float): probability
            n (int): number of occurrences

        Returns:
            float: probability after n occurrences
        """

        return 1 - (1 - p) ** n


    def generator_function(self, location: tuple, grid: object, config: object):

        person = Person(location, grid, config)

        for state, locations in self.initializations.items():
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


    def generate_movie(self, image_dir, video_file, fps = 25):
        image_files = [os.path.join(image_dir, img)
                    for img in os.listdir(image_dir)
                    if img.endswith(".png")]
        image_files.sort()

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps = fps)
        clip.write_videofile(video_file, codec = 'png')

        return
    
    ### generate_movie ###


    def run_simple_epidemic(self):
        """ Create population and run a simple epidemic.
        """
        # Define parameters. Model parameters are stored in seld.config_model
        # compute probability of getting disease and store in qr0
        r0 = self.config_model['r0']
        ne = self.config_model['de']
        ni = self.config_model['di'] # days infected
        n = ne + ni
        beta = InfectiousDiseaseModel.recurrent_p(1 - 1 / r0, n)
        self.config_model['beta'] = beta

        # set the natural death parameter
        b = self.config_model['b']
        if b < 0:
            real_pop = self.config_pop['real']
            if 'population_size' in real_pop.keys() and \
               'natural_death' in real_pop.keys():
                
                pop_size = real_pop['population_size']
                pop_death = real_pop['natural_death']

                if pop_size > 0:
                    b = pop_death / pop_size
                else:
                    b = 0
                # if

            else:
                b = 0

            # if
            # Set b to recurrent probability for days / year
            self.config_model['b'] = InfectiousDiseaseModel.recurrent_p(b, 365)

        # if

        # Compute daily disease mortality based on alfa
        alfa = self.config_model['alfa']
        self.config_model['pd'] = InfectiousDiseaseModel.recurrent_p(alfa, ni)

        # Compute daily disease mortality based on comorbidity
        c = self.config_model['c']
        self.config_model['pc'] = InfectiousDiseaseModel.recurrent_p(c, ni)

        # Create a grid generator
        generator = GridMatrixGenerator()

        # create a grid with appropriate number of columns and rows
        grid = generator.generate(
            grid_size = (self.rows, self.cols), 
            res_path = self.res_path, 
            icon_style = self.icon_style,
            config = self.config_model,
            generator_function = self.generator_function,
        )
        self.initial_seed(grid, 'I')

        grid.create_recorder(Thing.definitions, self.epochs)
    
        # define a grid viewer for the grid
        grid_viewer = GridViewMatrix(
            grid = grid, 
            definitions = Thing.definitions, 
            screen_size = (self.screen_width, self.screen_height),
        )
        
        grid_viewer.update_screen()

        image_dir = os.path.join(self.result_dir, 'images')
        while grid.ticks <= self.epochs:
            save_file = os.path.join(image_dir, f'model_run_{grid.ticks:04d}.png')
            pygame.image.save(grid_viewer.screen, save_file)

            grid_viewer.update_screen()
            grid.next_turn()
    
        # while

        # save all snapshots to file
        grid.recorder.to_csv(os.path.join(self.result_dir, 'model_output.csv'), sep=';')
        
        # create a movie from the saved images
        movie_file = os.path.join(self.result_dir, 'model-epidemic.avi')
        self.generate_movie(image_dir, movie_file)

        # plot the snapshots
        self.plot(grid.recorder, grid_viewer.definitions)

        # input('Press <enter> to quit')
        pygame.quit()
        
        return
        
    ### test_move_around ###


    def plot(self, df: pd.DataFrame, definitions: pd.DataFrame):  
        # plt.figure()
        colors = [(x[0]/255, x[1]/255, x[2]/255) for x in definitions[COL_COLOR]]
        df.plot(color = colors)
        plt.xlabel('t (days)')
        plt.ylabel('Numbere of persons')
        plt.title('Infectious Disease Model Run')
        plt.legend(loc='best')
        plt.savefig(os.path.join(self.result_dir, 'model_plot.png'))
        plt.show()

        return
    
    ### plot ###

### Class: InfectiousDiseaseModel ###

