import random

def get_value(dict: dict, key: str, default: str = None):

    if key in dict.keys():
        return dict[key]
    
    else:
        return default
    
    ### get_key_from_dict ###


def convert_coord(coord: str, max: int) -> int:
    result = -1
    coord = coord.lower().strip()
    if coord == 'r':
        result = int(random.random() * max)

    elif '/' in coord:
        teller, noemer = coord.split('/')
        teller = int(teller)
        noemer = int(noemer)
        if noemer > 0 and noemer >= teller:
            fraction = teller / noemer
            result = int(fraction * max)
        else:
            raise ValueError(f'Fraction {teller} / {noemer} incorrectly specified')

    else:
        result = int(coord)

    return result

### convert_coord ###


def prob(nb: int, prb: float):
    if nb > 0:
        result = random.random() < prb

    else:
        result = False

    return result

### prob ###


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


def inverse_p(p: float, n: int) -> float:
    """ Computes the inverse of recurrent probability.

    Args:
        p (float): probability
        n (int): number of occurrences

    Returns:
        float: probability after n occurrences
    """

    return 1 - (1 - p) ** n


