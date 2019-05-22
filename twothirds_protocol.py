#!python3

"""
The Two-thirds allocation protocol (for two binary identical families)

See: https://arxiv.org/abs/1709.02564 Theorem 3.14 for details.
"""

from functools import lru_cache
from collections import defaultdict
import fairness_criteria
from agents import *
from families import Family

def allocate(families:list, goods: set):
    """
    Run the protocol (see Section 3 in the paper) that guarantees to each family
    2/3-democratic 1-of-best-2 fairness.
    Currently, it works only for two identical families.
    :return a list of bundles - a bundle per family.


    >>> fairness_1_of_best_2 = fairness_criteria.OneOfBestC(2)
    >>> family1 = Family([BinaryAgent("wx",1),BinaryAgent("yz",1)], fairness_1_of_best_2)
    >>> (bundle1,bundle2) = allocate([family1, family1], "wxyz")
    >>> len(bundle1)
    2
    >>> len(bundle2)
    2
    """
    if len(families)!=2:
        raise("Currently only 2 families are supported")

    goods = set(goods)
    bundles = [set(), goods] # start, arbitrarily, with an allocation that gives all goods to family 2.

    total_num_of_members = sum([family.num_of_members for family in families])
    num_of_iterations = 2*total_num_of_members   # this should be sufficient to convergence if the families are identical
    for iteration in range(num_of_iterations):
        # If there is a good $g\in G_1$ for which $q_0(g) > q_1(g)$, move $g$ to $G_2$.
        allocate.trace("Currently, {} holds {} and {} holds {}".format(families[0].name, bundles[0], families[1].name, bundles[1]))
        change=False
        for g in list(bundles[0]):
            poor_in_2  = families[1].num_of_members_with(lambda member: member.value(g)>0 and member.value(bundles[1])==0)
            poor_in_1  = families[0].num_of_members_with(lambda member: member.value(g)>0 and member.value(bundles[0])==1)
            if poor_in_2>poor_in_1:
                allocate.trace("Moving {} from {} to {}, harming {} members in and helping {}.".format(g, families[0].name, families[1].name, poor_in_1, poor_in_2))
                bundles[0].remove(g)
                bundles[1].add(g)
                change=True
        for g in list(bundles[1]):
            poor_in_1 = families[0].num_of_members_with(lambda member: member.value(g)>0 and member.value(bundles[0])==0)
            poor_in_2 = families[1].num_of_members_with(lambda member: member.value(g)>0 and member.value(bundles[1])==1)
            if poor_in_1>poor_in_2:
                allocate.trace("Moving {} from {} to {}, harming {} members and helping {}.".format(g, families[1].name, families[0].name, poor_in_2, poor_in_1))
                bundles[1].remove(g)
                bundles[0].add(g)
                change=True
        if not change:
            break
    return bundles
allocate.trace = lambda *x: None  # To enable tracing, set allocate.trace=print






if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
