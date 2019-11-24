#!python3

"""
Enhanced RWAV protocol (for two binary families)

See: https://arxiv.org/abs/1709.02564 Theorem 3.13 for details.
"""

import fairness_criteria
from agents import *
from families import *
import rwav_protocol

import logging, sys
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# To enable tracing, logger.setLevel(logging.INFO)

def allocate(families:list, goods: set, threshold: float):
    """
    Run the Enhanced RWAV protocol (see Section 3 in the paper) on the given families.
    Currently only 2 families are supported.
    :return a list of bundles - a bundle per family.
    :param threshold: a number in [0,1].
      If there is a single good g that is wanted by at least this fraction of members in one of the families,
      then this family gets g and the other family gets the other goods.

    >>> fairness_1_of_best_2 = fairness_criteria.OneOfBestC(2)
    >>> family1 = Family([BinaryAgent({"w","x"},1),BinaryAgent({"x","y"},3),BinaryAgent({"y","z"},3), BinaryAgent({"w","v"},3)], fairness_1_of_best_2)
    >>> family2 = Family([BinaryAgent({"w","x"},5),BinaryAgent({"y","z"},5)], fairness_1_of_best_2)
    >>> (bundle1,bundle2) = allocate([family1, family2], ["v","w","x","y","z"], threshold=0.6)
    >>> sorted(bundle1)
    ['y']
    >>> sorted(bundle2)
    ['v', 'w', 'x', 'z']
    >>> (bundle2,bundle1) = allocate([family2, family1], ["v","w","x","y","z"], threshold=0.6)
    >>> sorted(bundle1)
    ['y']
    >>> sorted(bundle2)
    ['v', 'w', 'x', 'z']
    """
    if len(families)!=2:
        raise("Currently only 2 families are supported")

    goods = set(goods)
    thresholds = [threshold*family.num_of_members for family in families]
    for g in goods:
        nums = [family.num_of_members_with(lambda member: member.value(g)>0)
                for family in families]
        if nums[0] >= thresholds[0]:
            bundle1 = set(g)
            bundle2 = goods.difference(bundle1)
            logger.info("{} out of {} members in {} want {}, so group 1 gets {} and group 2 gets the rest".format(
                nums[0],     families[0].num_of_members,     families[0].name, g,                  g))
            return (bundle1,bundle2)
        elif nums[1] >= thresholds[1]:
            bundle2 = set(g)
            bundle1 = goods.difference(bundle2)
            logger.info("{} out of {} members in {} want {}, so group 2 gets {} and group 1 gets the rest".format(
                nums[1],     families[1].num_of_members,     families[1].name, g,                  g))
            return (bundle1,bundle2)
    return rwav_protocol.allocate(families, goods)



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
