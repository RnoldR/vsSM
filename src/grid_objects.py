# Code initialisatie: logging
import logging
logger = logging.getLogger()

import random
import numpy as np
import pandas as pd

from grid import Grid
from grid_thing import Thing

from grid_thing_data import COL_NAME, COL_DESCRIPTION, COL_CATEGORY, \
    COL_CHAR, COL_DATA, COL_ICON

from lib_vsfsm import vsFSM

# Infection pareameters in days
# infected_time = 1
# contagious_time = 21
# immunity_time = 365
# rho = 0.1 # virulence
# pm = 0.02 / contagious_time
# pz = 1 - pm


def prob(nb: int, prb: float):
    if nb > 0:
        result = random.random() < prb

    else:
        result = False

    # print(nb, prb, result)

    return result
### prob ###


class Person(Thing):
    def __init__(self, location: tuple, grid: Grid, config: dict):
        super().__init__(location, grid)

        self.name = "Person"
        self.type: str = self.get_type() # __class__.__name__
        self.name: str = f'{self.__class__.__name__}'
        self.description: str = f'{self.__class__.__name__}_{self.row}_{self.col}'
        self.category: int = ''
        self.char: str =''
        self.data: str = ''
        self.icons: object = ''

        # infection parameters
        days_exposure = config['de']
        days_infection = config['di']
        days_recovered = config['dr']
        beta = config['beta'] # Probability to get infected per day

        alfa = config['pm']

        # Create state machine and add states
        self.fsm = vsFSM()
        self.states = []
        for x in super().definitions.index:
            self.states.append(x)
        self.fsm.add_states(self.states)

        # For each state add transitions
        self.fsm.add_transition('S', lambda inputs: prob(inputs['Neighbours']['I'], beta), 'E')
        self.fsm.add_transition('S', lambda inputs: inputs['Neighbours']['I'] == 0, 'S')
        
        self.fsm.add_transition('E', lambda inputs: grid.ticks - inputs['Ticker'] < days_exposure-1, 'E')
        self.fsm.add_transition('E', lambda inputs: grid.ticks - inputs['Ticker'] >= days_exposure-1, 'I')

        self.fsm.add_transition('I', lambda inputs: prob(1, alfa), 'D')
        self.fsm.add_transition('I', lambda inputs: grid.ticks - inputs['Ticker'] < days_infection-1, 'I')
        self.fsm.add_transition('I', lambda inputs: grid.ticks - inputs['Ticker'] >= days_infection-1, 'R')

        self.fsm.add_transition('R', lambda inputs: grid.ticks - inputs['Ticker'] < days_recovered-1, 'R')
        self.fsm.add_transition('R', lambda inputs: grid.ticks - inputs['Ticker'] >= days_recovered-1, 'S')

        self.fsm.add_transition('D', lambda inputs: True, 'D')

        # Add input values
        self.fsm.set_input('Row', self.row)
        self.fsm.set_input('Col', self.col)
        self.fsm.set_input('Grid', self.grid)
        self.fsm.set_input('Interrupt', False)
        self.fsm.set_start_state('S')
        
        return
    
    ### __init__ ###


    def get_state(self):

        return self.fsm.get_current_state()
    
    ### get_state ###


    def set_state(self, state):

        self.fsm.set_current_state(state)

        return
    
    ### set_state ###

    def neighbours(self, ridx: int, cidx: int, radius: int = 1):
        # pre-fill all states with zero
        states = {'Count': 0}
        for state in self.states:
            states[state] = 0

        # count the number of occurrences for each cell
        for row in range(ridx - radius, ridx + radius + 1):
            for col in range(cidx - radius, cidx + radius + 1):
                if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
                    states['Count'] += 1
                    state = self.grid.matrix[row, col].fsm.get_current_state()
                    if state in states.keys():
                        states[state] += 1

                    else:
                        states[state] = 0

                    # if
                # if
            # for
        # for

        return states

    ### neighbours ###


    def count_states(self):
        # pre-fill all states with zero
        states = {}
        for state in self.grid.matrix[0, 0].states:
            states[state] = 0

        # count state of all cells
        for row in range(self.rows):
            for col in range(self.cols):
                state = self.grid.matrix[row, col].get_current_state()
                states[state] += 1
            # for
        # for

        return states
    
    ### count_states ###


    def evaluate(self):

        # Pre evaluation
        cell = self.grid.matrix[self.row, self.col]
        neigbour_states = self.neighbours(self.row, self.col)
        cell.fsm.set_input('Neighbours', neigbour_states)

        # cell = self.grid.matrix[self.row, self.col]
        self.fsm.evaluate()

        return
    
    ### evaluate ###


    def next_turn(self):
        super().next_turn()

        self.evaluate()

        return
    
    ### next_turn ###

### Class: Person ###
