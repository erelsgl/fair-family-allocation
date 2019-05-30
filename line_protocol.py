#!python3

"""
The line-allocation protocol:
* 1/2-democratic EF1 for two families with general monotone agents;
* 1/k-democratic fair for k families with additive agents.

See: https://arxiv.org/abs/1709.02564 Theorems 4.2 and 5.8.
"""

from agents import *
from families import Family
import fairness_criteria


trace = lambda *x: None  # To enable tracing, set trace=print


def allocate(families:list, goods:list)->list:
    """
    Order the goods on a line and allocate them in 1/k-democratic fair way among k families,
    based on the fairness-criterion of each family.
    :return a list of bundles - a bundle per family.

    NOTE: The algorithm is guaranteed to finish with an allocation in the following cases:
       Case A: there are two families, and the fairness criterion is EF1 or weaker
          (1/2-fraction-MMS, 1-of-3-MMS, MMS if the agents are binary, or PROP1?).
          This is proved in Theoren 4.2 and Corollary 4.6.
       Case B: there are k familis, and the fairness criterion is one of
          (1/k-fraction-MMS, 1-of-(2k-1)-MMS, MMS if the agents are binary, or PROP[k-1]).
          This is proved in Theorem 5.8.
       In other cases, the algorithm behavior is undefined.


    >>> fairness_PROP1 = fairness_criteria.ProportionalExceptC(num_of_agents=2,c=1)
    >>> family1 = Family([BinaryAgent({"w","x"},1),BinaryAgent({"x","y"},2),BinaryAgent({"y","z"},3), BinaryAgent({"z","w"},4)], fairness_criterion=fairness_PROP1, name="Family 1")
    >>> family2 = Family([BinaryAgent({"w","z"},2),BinaryAgent({"z","y"},3)], fairness_criterion=fairness_PROP1, name="Family 2")
    >>> (bundle1,bundle2) = allocate([family1, family2], ["w","x","y","z"])
    >>> sorted(bundle1)
    ['w']
    >>> sorted(bundle2)
    ['x', 'y', 'z']
    >>> (bundle1,bundle2) = allocate([family2, family1], ["x","w","y","z"])
    >>> sorted(bundle1)
    ['y', 'z']
    >>> sorted(bundle2)
    ['w', 'x']
    """
    k = len(families)

    if k==1:
        family = families[0]
        trace("   {} gets the remaining bundle".format(family.name))
        return [set(goods)]

    goods=list(goods)  # order the goods on a line
    left_sequence = list()
    right_sequence = list(goods)
    for good in goods:
        trace("\nCurrent partition:  {} | {}:".format(left_sequence,right_sequence))
        left_bundle = set(left_sequence)
        right_bundle = set(right_sequence)
        for family_index in range(len(families)):
            family = families[family_index]
            num_of_happy_members = family.num_of_happy_members(left_bundle, [right_bundle])
            trace("   {}: {}/{} members think the left bundle is {}".format(
                family.name, num_of_happy_members, family.num_of_members, family.fairness_criterion.abbreviation))
            if num_of_happy_members*k >= family.num_of_members:
                trace("   {} gets the left bundle".format(family.name))
                other_families = list(families)
                del other_families[family_index]
                bundles = allocate(other_families, right_sequence)
                bundles.insert (family_index, left_bundle)
                return bundles
        left_sequence.append(good)
        right_sequence.pop(0)
    raise AssertionError(
        "No family is willing to accept the set of all goods - the fairness criteria are probably too strong")



if __name__ == "__main__":
    import doctest
    # trace = print
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
