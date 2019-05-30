#!python3

"""
This program exhaustively searches for a negative example to the two-thirds conjecture.

See: https://arxiv.org/abs/1709.02564 Conjecture 3.12 for details.
"""

import fairness_criteria
from agents import BinaryAgent
from families import Family
import copy, itertools, utils
from partitions import powerset, partitions_to_exactly_c

fairness_1_of_best_2 = fairness_criteria.OneOfBestC(2)

trace = lambda *x: None  # To enable tracing, set trace=print


def demo(family:Family, goods:set):
    family1 = copy.copy(family); family1.name="Group 1"
    family2 = copy.copy(family); family2.name="Group 2"
    utils.demo(twothirds_protocol.allocate, [family1, family2], goods)

def all_agents(goods:list):
    """
    Generates all possible agents that want exactly two goods from the given list.

    >>> len(list(all_agents("xyz")))
    3
    >>> len(list(all_agents("wxyz")))
    6
    >>> len(list(all_agents("vwxyz")))
    10
    """
    for desired_goods in itertools.combinations(goods, 2):
        yield BinaryAgent(desired_goods,1)

def all_families(goods:list):
    """
    Generates all possible non-empty families of agents, with at most one agent of each type.

    >>> len(list(all_families("xyz")))
    7
    >>> len(list(all_families("wxyz")))
    63
    """
    index = 1
    for members in powerset(all_agents(goods)):
        if len(members)>0:
            family = Family(members, fairness_1_of_best_2, name=index)
            index += 1
            yield family


FRACTION_THRESHOLD = 2/3
def is_conjecture_true_for(family1:Family, family2:Family, goods:set)->bool:
    """
    Checks if the 2/3 conjecture true for the given two families.
    """
    for allocation in partitions_to_exactly_c(list(goods), c=2):
        if family1.fraction_of_happy_members(allocation[0], allocation)>=FRACTION_THRESHOLD \
            and family2.fraction_of_happy_members(allocation[1], allocation)>=FRACTION_THRESHOLD:
            return True # Allocation (0,1) is 2/3-democratic fair
        if family1.fraction_of_happy_members(allocation[1], allocation)>=FRACTION_THRESHOLD \
            and family2.fraction_of_happy_members(allocation[0], allocation)>=FRACTION_THRESHOLD:
            return True # Allocation (1,0) is 2/3-democratic fair
    return False


def check_conjecture_for(goods:str):
    """
    Checks  the 2/3 conjecture for the given set of goods.
    """
    print("Checking the 2/3 conjecture for {} goods...".format(len(goods)))
    for family1 in all_families(goods):
        for family2 in all_families(goods):
            if family1.name < family2.name:
                if not is_conjecture_true_for(family1,family2, goods):
                    print("The 2/3 conjecture is false for the following families:")
                    print(family1)
                    print(family2)
                    return
                else:
                    trace("Conjecture is true for family {} vs family {}".format(family1.name, family2.name))
    print("The 2/3 conjecture is true for {} goods".format(len(goods)))


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
    trace = print   # comment-out this line for a silent run; uncomment for trace
    # check_conjecture_for("xyz")
    # check_conjecture_for("wxyz")
    # check_conjecture_for("vwxyz")
    # check_conjecture_for("uvwxyz")

