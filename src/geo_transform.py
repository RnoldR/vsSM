# import logging
from create_logger import create_logger
logger = create_logger.create_log('grid-vehicles.log')

import os
import time
import yaml
import pygame
import shapely
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
# import moviepy.video.io.ImageSequenceClip

from itertools import chain
from datetime import datetime

from grid_viewer import GridViewMatrix
from grid_generators import GridMatrixGenerator
from grid_thing import Thing
from grid_objects import Person

from idm_utils import recurrent_p, prob

from grid_thing_data import COL_NAME, COL_DESCRIPTION, COL_CATEGORY, \
    COL_CHAR, COL_DATA, COL_ICON, COL_COLOR


class GeoGems(object):
    def __init__(self, res_path: str, config_file: str, geo_pad: str):
        super().__init__()

        # read config file and assign to instance variables
        filename = os.path.join(res_path, 'config', config_file)
        with open(filename) as infile:
            config = yaml.safe_load(infile)

        self.config_screen = config['Screen']
        self.config_pop = config['Population']
        self.config_model = config['Infectionmodel']

        # Read screen parameters
        self.res_path = res_path
        self.geo_pad = geo_pad
        self.screen_width = self.config_screen['screen_width']
        self.screen_height = self.config_screen['screen_height']
        self.rows = self.config_screen['rows']
        self.cols = self.config_screen['cols']
        self.icon_style = self.config_screen['icon_style']

        # Get model parameters
        self.epochs = self.config_model['epochs']
        self.initializations = self.config_model['initialization']

        # read Thing definition file
        Thing.set_definitions(res_path, self.icon_style)  
        self.states = [x for x in Thing.definitions.index]

        # create directory to save results to
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S").replace(' ', '_')
        self.result_dir = os.path.join(res_path, 'results', now)
        os.makedirs(os.path.join(self.result_dir, 'images'))
        print('Results will be written to', self.result_dir)

        return
    
    ### __init__###


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


    def get_borders(self, pad: str):
        def transformation(x):
            x[:,0] = self.cols * (x[:,0] - lrx) / xrange
            x[:,1] = self.rows * (x[:,1] - lry) / yrange

            return x
        
        def to_coords(multipolygon):
            for polygon in list(multipolygon.geoms):
                yield from polygon.exterior.coords[:-1]
                yield from chain.from_iterable(interior.coords[:-1] for interior in polygon.interiors)


        
        df = gpd.read_file(pad, layer = 'cbs_gemeente_2022_gegeneraliseerd')
        df.insert(len(df.columns) - 1, 'geom', None)
        print(df.columns)
        df['geom'] = df['geometry']
        bounds = df.total_bounds
        lrx = bounds[0]
        lry = bounds[1]
        ulx = bounds[2]
        uly = bounds[3]
        xrange = ulx - lrx
        yrange = uly - lry
 
        print('\nx:', lrx, lry, xrange)
        print('y:', ulx, uly,yrange)


        # df['geometry'] = shapely.transform(df['geometry'], transformation)
        df['geometry'] = shapely.transform(df['geom'], transformation)
        pp = []
        for idx, multi_polygon in df['geometry'].items():
            # print('***********')
            # print(type(poly))
            # print(poly.shape)

            # methods 1
            poly_list = list(to_coords(multi_polygon))
            df.at[idx, 'geometry'] = [poly_list]

            # method 2
            # poly_mapped = shapely.geometry.mapping(poly)
            # poly_coordinates = poly_mapped['coordinates'][0]
            # poly_list = [(coords[0], coords[1]) for coords in poly_coordinates]

            # print(poly_list[:10])

            # pp.append(poly_list)

        


        fig, ax = plt.subplots(figsize=(8,8))

        df.plot(ax=ax, facecolor='none', edgecolor='blue')
        plt.show()


        # bounds = df.total_bounds
        # lrx = bounds[0]
        # lry = bounds[1]
        # ulx = bounds[2]
        # uly = bounds[3]
        # xrange = ulx - lrx
        # yrange = uly - lry
 
        # print('\nx:', lrx, lry, xrange)
        # print('y:', ulx, uly,yrange)

        return pp
    
    ### get_borders ###


    def run_simple_epidemic(self):
        """ Create population and run a simple epidemic.
        """
        # Define parameters. Model parameters are stored in seld.config_model
        # compute probability of getting disease and store in qr0
        r0 = self.config_model['r0']
        ne = self.config_model['de']
        ni = self.config_model['di'] # days infected
        n = ne + ni
        beta = recurrent_p(1 - 1 / r0, n)
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
        # if

        # Set b to recurrent probability for days / year
        pb = recurrent_p(b, 365)
        self.config_model['pb'] = pb
        
        # Compute daily disease mortality based on alfa
        alfa = self.config_model['alfa']
        self.config_model['pd'] = recurrent_p(alfa, ni)

        # Compute daily disease mortality based on comorbidity
        c = self.config_model['c']
        self.config_model['pc'] = recurrent_p(c, ni)

        # Create dictionary of parameters to display
        pars = {}
        pars['r0'] = f'{r0:7d}'
        pars['β'] = f'{beta:7.4f}'
        pars['Days exposed'] = f'{ne:7d}'
        pars['Days infected'] = f'{ni:7d}'
        pars['Natural mort. (b)'] = f'{b:7.4f}'
        pars['Disease mort. (α)'] = f'{alfa:7.4f}'
        pars['Comortality (pc)'] = f'{c:7.4f}'

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

        grid_viewer.update_screen(pars)

        borders = self.get_borders(self.geo_pad)
        print(type(borders))
        for polygon in borders:
            grid_viewer.test_polygon(polygon)

        image_dir = os.path.join(self.result_dir, 'images')
        while grid.ticks <= self.epochs:
            input('Next')
            # save_file = os.path.join(image_dir, f'model_run_{grid.ticks:04d}.png')
            # pygame.image.save(grid_viewer.screen, save_file)

            grid_viewer.update_screen(pars)
            grid.next_turn()
    
        # while

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


# import logging
from create_logger import create_logger

res_path = '/media/i-files/home/arnold/development/python/vsSM'
logfile = os.path.join(res_path, 'geo-transform.log')
logger = create_logger.create_log(logfile)
geo_pkg = '/media/i-files/data/geo_nl_cbs/gebieden-gpkg/cbsgebiedsindelingen2022.gpkg'

gg = GeoGems(res_path, 'partial-vaccination.config', geo_pkg)
gg.get_borders(geo_pkg)
gg.run_simple_epidemic()