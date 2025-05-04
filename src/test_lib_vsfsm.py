import time
from lib_vsfsm import vsFSM

def do_fast():
    print('> Fast')

def do_slow():
    print('> Slow')

def do_stop():
    print('> Stop')

def do_back():
    print('> Back')

def do_turn():
    print('> Turn')

def do_halt():
    print('> Halt')

# Constants
# Distances in cm's
SP_SAFE = 60
SP_UNSAFE = 30

# Durations in seconds
DR_STOP = 1
DR_BACK = 0.5

# Create state machine and add states
fsm = vsFSM()
fsm.add_states(['Fast', 'Slow', 'Stop', 'Back', 'Turn', 'Halt'])

# For each state add transitions
fsm.add_transition('Fast', lambda inputs: inputs['Interrupt'], 'Halt')
fsm.add_transition('Fast', lambda inputs: inputs['Distance'] >= SP_SAFE, 'Fast')
fsm.add_transition('Fast', lambda inputs: inputs['Distance'] < SP_SAFE, 'Slow')

fsm.add_transition('Slow', lambda inputs: inputs['Interrupt'], 'Halt')
fsm.add_transition('Slow', lambda inputs: inputs['Distance'] >= SP_SAFE, 'Fast')
fsm.add_transition('Slow', lambda inputs: SP_UNSAFE <= inputs['Distance'] < SP_SAFE, 'Slow')
fsm.add_transition('Slow', lambda inputs: inputs['Distance'] < SP_UNSAFE, 'Stop')

fsm.add_transition('Stop', lambda inputs: inputs['Interrupt'], 'Halt')
fsm.add_transition('Stop', lambda inputs: time.time() - inputs['Timer'] < DR_STOP, 'Stop')
fsm.add_transition('Stop', lambda inputs: time.time() - inputs['Timer'] >= DR_STOP, 'Back')

fsm.add_transition('Back', lambda inputs: inputs['Interrupt'], 'Halt')
fsm.add_transition('Back', lambda inputs: time.time() - inputs['Timer'] < DR_BACK, 'Back')
fsm.add_transition('Back', lambda inputs: time.time() - inputs['Timer'] >= DR_BACK, 'Turn')

fsm.add_transition('Turn', lambda inputs: inputs['Interrupt'], 'Halt')
fsm.add_transition('Turn', lambda inputs: inputs['Distance'] < SP_UNSAFE, 'Halt')
fsm.add_transition('Turn', lambda inputs: inputs['Distance'] >= SP_UNSAFE, 'Slow')

fsm.add_transition('Halt', lambda inputs: inputs['Interrupt'], 'Halt')

# Add input values
fsm.set_input('Distance', 20)
fsm.set_input('Timer', time.time())
fsm.set_input('Interrupt', False)
fsm.set_start_state('Fast')

print('Start state: ', fsm.start_state)

halter = time.time()
while fsm.get_current_state() != 'Halt':
    print(f'Current state: {fsm.get_current_state()}, ticks: {fsm.get_input('Ticks')}')
    fsm.evaluate()

    if fsm.state_changed: #new_state != fsm.get_current_state():
        print('New state:', fsm.get_current_state())
        
        # set Timer because some states are time limited
        fsm.set_input('Timer', time.time())
                
    # if

    if fsm.get_current_state() == 'Fast':
        do_fast()
    
    elif fsm.get_current_state() == 'Slow':
        do_slow()
    
    elif fsm.get_current_state() == 'Stop':
        do_stop()
    
    elif fsm.get_current_state() == 'Back':
        do_back()
    
    elif fsm.get_current_state() == 'Turn':
        do_turn()
    
    elif fsm.get_current_state() == 'Halt':
        do_halt()

    else:
        raise ValueError(f'Selected a not foreseen state: {fsm.get_current_state()}')
    

    time.sleep(0.24)

    if time.time() - halter > 3:
        fsm.set_input('Interrupt', True)

