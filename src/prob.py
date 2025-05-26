def q(p: float, n: int) -> float:
    """ Defines recurrent probability after n occurrences

    Args:
        p (float): probability
        n (int): number of occurrences

    Returns:
        float: probability after n occurrences
    """

    return 1 - (1 - p) ** n


def p(q: float, n: int) -> float:
    """ Returns probability when recurrent probability is known.

        Inverse of p().

    Args:
        q (float): recurrent probability
        n (int): number of occurrences

    Returns:
        float: single probability
    """

    return (1 - (1 - q) ** (1 / n))


prob = 0.9
occurrences = 10
q_prob = p(prob, occurrences)

# compute inverse
p_prob = q(q_prob, occurrences)

print('p:  ', prob)
print('n:  ', occurrences)
print('q:  ', q_prob)
print('rev:  ', p_prob)
