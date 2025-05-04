import time
import json
import random

import numpy as np
import matplotlib.pyplot as plt
from lib_vsfsm import vsFSM, vsFSMMatrix

def do_x():
    print('> X')

def do_i():
    print('> I')

def do_Y():
    print('> Y')

def do_z():
    print('> Z')

def create_cell(row, col, mat):
    def prob(nb: int, prb: float):
        if nb > 0:
            result = random.random() < prb

        else:
            result = False

        # print(nb, prb, result)

        return result
    ### prob ###

    # Create state machine and add states
    fsm = vsFSM()
    fsm.add_states(['X', 'I', 'Y', 'Z', 'M'])

    # For each state add transitions
    fsm.add_transition('X', lambda inputs: prob(inputs['Neighbours']['Y'], RHO), 'I')
    fsm.add_transition('X', lambda inputs: inputs['Neighbours']['Y'] == 0, 'X')
    
    fsm.add_transition('I', lambda inputs: matrix.ticks - inputs['Ticker'] < INCUBATION_TIME-1, 'I')
    fsm.add_transition('I', lambda inputs: matrix.ticks - inputs['Ticker'] >= INCUBATION_TIME-1, 'Y')

    fsm.add_transition('Y', lambda inputs: prob(1, PM), 'M')
    fsm.add_transition('Y', lambda inputs: matrix.ticks - inputs['Ticker'] >= INFECTION_DURATION-1, 'Z')
    fsm.add_transition('Y', lambda inputs: matrix.ticks - inputs['Ticker'] < INFECTION_DURATION-1, 'Y')

    fsm.add_transition('Z', lambda inputs: matrix.ticks - inputs['Ticker'] < IMMUNITY-1, 'Z')
    fsm.add_transition('Z', lambda inputs: matrix.ticks - inputs['Ticker'] >= IMMUNITY-1, 'X')

    fsm.add_transition('M', lambda inputs: True, 'M')

    # Add input values
    fsm.set_input('Row', row)
    fsm.set_input('Col', col)
    fsm.set_input('Matrix', mat)
    fsm.set_input('Interrupt', False)
    fsm.set_start_state('X')

    return fsm

### create_cell ###


def plot(data):
    d = data.keys()
    n = len(d)

    x = np.zeros(n)
    i = np.zeros(n)
    y = np.zeros(n)
    m = np.zeros(n)
    z = np.zeros(n)

    j = 0
    for key, value in data.items():
        x[j] = value['X']
        i[j] = value['I']
        y[j] = value['Y']
        m[j] = value['M']
        z[j] = value['Z']
        j+=1
    # for

    plt.plot(d, x, 'b', label = 'Vatbaar')
    plt.plot(d, i, 'orange', label = 'Geinfecteerd')
    plt.plot(d, y, 'r', label = 'Besmettelijk')
    plt.plot(d, m, 'k', label = 'Dood')
    plt.plot(d, z, 'g', label = 'Immuun')

    plt.legend(loc='upper left')

    plt.show()

    return

### plot ###


# Constants
NROWS = 100
NCOLS = 100

# Infection pareameters in days
INCUBATION_TIME = 1
INFECTION_DURATION = 21
IMMUNITY = 365
RHO = 0.9 # virulence
PM = 0.02 / INFECTION_DURATION
PZ = 1 - PM
EPOCHS = 800

print('Initializing matrix')
matrix = vsFSMMatrix(NROWS, NCOLS, vsFSM)

print('Filling...')
matrix.fill(create_cell)

# Infect first cell
matrix.matrix[0, 0].set_start_state('Y')

# print initial count of states
states = matrix.count_states()
print(f'Day:{matrix.ticks:5} - {states}')

data = {}

# Loop for some days
while matrix.ticks < EPOCHS:
    for r in range(matrix.rows):
        for c in range(matrix.cols):
            pass
            # print(r, c, matrix.matrix[r, c].get_input('Ticker'))

    matrix.evaluate()

    # print state count after evaluation
    states = matrix.count_states()
    data[matrix.ticks] = states

    print(f'Day:{matrix.ticks:5} - {states}')

# while

with open('logfile.txt', 'w') as logfile:
    json.dump(data, logfile)

plot(data)