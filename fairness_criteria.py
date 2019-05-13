#!python3

"""
Defines various useful fairness criteria to use with fair allocation algorithms.

A fairness criterion for a binary instance is an integer function s(r),
where r is the number of goods that an agent values at 1,
and s is the number of goods that this agent should receive in order to satisfy the criterion.
"""

import math

def one_of_best_c(c:int):
    """
    Returns the fairness criterion "1 out of best c".

    >>> criterion=one_of_best_c(3)
    >>> [criterion(r) for r in range(10)]
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    """
    return lambda r: 1 if r >= c else 0

def maximin_share_one_of_c(c:int):
    """
    Returns the fairness criterion "1 of c maximin-share".

    >>> criterion=maximin_share_one_of_c(3)
    >>> [criterion(r) for r in range(10)]
    [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
    """
    return lambda r: math.floor(r/c)



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
