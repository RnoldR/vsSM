import time
import numpy as np

# State descriptions
from lib_vssm import vsM

class vsFSM(vsM):
    def __init__(self):
        super(vsFSM, self).__init__()

        return
    
    ### __init__ ###
    
    
    def add_transition(self,
                       state_name: str, 
                       condition: any, 
                       output: str,
                      ):
        
        if state_name not in self.states.keys():
            raise ValueError(f'State not yet added: {state_name}')
        
        # generate unique state name
        i = 1
        while i in self.states[state_name].keys():
            i += 1

        # create transition dictionary
        transition = {'condition': condition,
                      'output': output}
        
        # add it to the state
        self.states[state_name][i] = transition

        return
    
    ### add_transition ###
    
    
    def evaluate(self):
        # evaluate super function
        super(vsFSM, self).evaluate()

        # get transition from current state
        state = self.states[self.current_state]
   
        # iterate thru all transitions
        for transition in state.keys():
            # Find and evaluate the condition with the inputs
            func = state[transition]['condition']
            result = func(self.inputs)

            # if result is True return output
            if result:
                if self.state_changed:
                    
                    # set Timer because some states are time limited
                    self.set_input('Timer', time.time())
                    self.set_input('Ticker', self.get_input('Ticks'))
                    
                # if

                self.set_current_state(state[transition]['output'])

                break

        # for

        return None
    
    ### evaluate ###

### Class: vsFSM ###
    
################################################################################

class vsFSMMatrix():
    def __init__(self, rows: int, cols: int, type: vsM):
        self.rows = rows
        self.cols = cols
        self.ticks = 0
        self.matrix = np.empty((self.rows, self.cols), dtype = type)

        return
    
    ### __init___ ###

    
    def fill(self, function):
        for r in range(self.rows):
            for c in range(self.cols):
                self.matrix[r, c] = function(r, c, self)

            # for
        # for

        return
    
    ### fill ###


    def neighbours(self, ridx: int, cidx: int, radius: int = 1):
        # pre-fill all states with zero
        states = {'Count': 0}
        for state in self.matrix[0, 0].states:
            states[state] = 0

        # count the number of occurrences for each cell
        for r in range(ridx - radius, ridx + radius + 1):
            for c in range(cidx - radius, cidx + radius + 1):
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    states['Count'] += 1
                    state = self.matrix[r, c].get_current_state()
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
        for state in self.matrix[0, 0].states:
            states[state] = 0

        # count state of all cells
        for r in range(self.rows):
            for c in range(self.cols):
                state = self.matrix[r, c].get_current_state()
                states[state] += 1
            # for
        # for

        return states
    
    ### count_states ###


    def evaluate(self):
        self.ticks += 1

        # Pre evaluation
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.matrix[r, c]
                neigbour_states = self.neighbours(r, c)
                cell.set_input('Neighbours', neigbour_states)
            # for
        # for

        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.matrix[r, c]
                cell.evaluate()
            # for
        # for

        return
    
    ### evaluate ###