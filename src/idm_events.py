from idm_utils import convert_coord, get_value

class Event(object):
    def __init__(self, event: dict, rows: int, cols: int):
        super().__init__()

        # set name of the event
        self.name = str(event['name'])

        # get and check event type
        event_type = str(event['type']).lower().strip()
        if event_type not in ['infection', 'vaccination']:
            raise ValueError(f'Event type can only be "infection" or "vaccination"')
        
        self.type = event_type

        # get event time, should be integer
        self.time = int(event['time'])

        # get and convert the event coordinates
        loc = event['location']
        if self.type == 'infection':
            # only one location present (row, col)
            r = convert_coord(str(loc[0]), rows)
            c = convert_coord(str(loc[1]), cols)

            self.location = (r, c)

            self.value = event['value']

        elif self.type == 'vaccination':
            # location should be rectangle of format: ((rul, cul), (rll, cll))
            rul = convert_coord(str(loc[0][0]), rows)
            cul = convert_coord(str(loc[0][1]), cols)
            rll = convert_coord(str(loc[1][0]), rows)
            cll = convert_coord(str(loc[1][1]), cols)
            
            self.location = ((rul, cul), (rll, cll))
    
            self.value = float(event['value'])

        else:
            pass # should be error but that has already been checked

        return
    
    ### __init__ ###
    
### Class: Event ###


class Events(object):
    def __init__(self, config: dict, rows: int, cols: int):
        super().__init__()

        self.calender = {}

        for key, value in config.items():
            value['name'] = key
            event = Event(value, rows, cols)

            self.insert_event(event)
            
        return
    
    ### __init__ ###


    def insert_event(self, event: Event):

        day = event.time
        if day not in self.calender.keys():
            self.calender[day] = [event]

        else:
            self.calender[day].append(event)

        return
    
    ### insert_event ###


    def has_events(self, time: int):
        if time in self.calender.keys():
            return True

        return False
    
    ### has_event ###


    def get_events(self, day: int):
        if self.has_events(day):
            return self.calender[day]
        
        else:
            return []

### Class: Events ###