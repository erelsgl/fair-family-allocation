#!python3

"""
Implementation of the RWAV protocol - Round-Robin with Approval Voting.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import numpy as np, math
from functools import lru_cache
from collections import defaultdict


@lru_cache(maxsize=None)
def binom(n:int, k:int)->int:
    """
    A fast way to calculate binomial coefficients by Andrew Dalke.
    See http://stackoverflow.com/questions/3025162/statistics-combinations-in-python

    NOTE: scipy.special.binom returns a float64 rather than an int.

    >>> binom(0,5)
    0
    >>> binom(5,0)
    1
    >>> binom(5,3)
    10
    >>> binom(5,5)
    1
    >>> binom(5,6)
    0
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

@lru_cache(maxsize=None)
def balance(r:int, s:int)->float:
    """
    Calculates the function B(r,s), which represents
       the balance of a user with r remaining goods and s missing goods.
    Uses the recurrence relation in https://arxiv.org/abs/1709.02564 .

    >>> balance(0,0)
    1
    >>> balance(1,1)
    0.5
    >>> balance(1,0)
    1
    >>> balance(0,1)
    0
    >>> balance(3,2)
    0.375
    >>> balance(0,-2)
    1
    >>> balance(-1,1)
    0
    """
    if (s<=0): return 1
    if (s>r): return 0
    val1 = (balance(r-1,s)+balance(r-1,s-1))/2
    val2 = balance(r-2,s-1)
    return min(val1,val2)

def weight(r:int, s:int)->float:
    """
    Calculates the function B(r,s), which represents
       the voting weight of a user with r remaining goods and s missing goods.
    Uses the recurrence relation in https://arxiv.org/abs/1709.02564 .

    >>> float(weight(4,0))
    0.0
    >>> float(weight(0,2))
    0.0
    >>> weight(1,1)
    0.5
    >>> weight(4,2)
    0.25
    >>> weight(4,3)
    0.0
    >>> float(weight(4,-2))
    0.0
    """
    return balance(r,s)-balance(r-1,s)



class BinaryAgent:
    """
    Represents an agent with binary valuations, or several agents with the same binary valuations.
    """

    def __init__(self, desired_goods:set, cardinality:int=1):
        """
        Initializes an agent with a given set of desired goods.
        :param desired_goods: a set of strings - each string is a good.
        :param cardinality: the number of agents with the same set of desired goods.
        """
        self.desired_goods = set(desired_goods)
        self.cardinality = cardinality

    def value(self, goods:set)->int:
        """
        Calculates the agent's value for the given set of goods.

        >>> BinaryAgent({"x","y","z"}).value({"w","x","y"})
        2
        >>> BinaryAgent({"x","y","z"}).value({"x","y"})
        2
        >>> BinaryAgent({"x","y","z"}).value({"w"})
        0
        >>> BinaryAgent({"x","y","z"}).value(set())
        0
        >>> BinaryAgent(set()).value({"x","y","z"})
        0
        """
        if isinstance(goods,set):
            return len(self.desired_goods.intersection(goods))
        else:
            raise ValueError("goods must be a set")

    def total_value(self):
        return len(self.desired_goods)

    def __repr__(self):
        return "{} agents who want {}".format(self.cardinality, sorted(self.desired_goods))


class BinaryFamily:
    """
    Represents a family of binary agents with a specific fairness criterion.

    >>> fairness_1_of_best_2 = lambda r: 1 if r>=2 else 0
    >>> BinaryFamily([BinaryAgent({"x", "y"}, 2), BinaryAgent({"z", "w"}, 1)], fairness_1_of_best_2)
    2 agents who want ['x', 'y'], 1 agents who want ['w', 'z']
    """
    def __init__(self, members:list, fairness_criterion):
        """
        Initializes a family with the given list of agents.
        :param members: a list of BinaryAgent objects.
        :param fairness_criterion: a function that maps the agent's total value (- number of desired goods)
                                to the agent's target value (- number of desired goods the family should have so that the agent is happy)
        """
        self.members = list(members)
        self.allocated_goods = set()
        for member in self.members:
            member.target_value = fairness_criterion(member.total_value())
        self.trace = lambda *x: None     # to trace, set self.trace = print

    def take_good(self, good:str):
        """
        Add the given good to the family's bundle.
        """
        self.allocated_goods.add(good)

    def discard_goods(self):
        """
        Reset the family's bundle to an empty bundle.
        """
        self.allocated_goods = set()

    def choose_good(self, remaining_goods:set)->str:
        """
        The family chooses a good from the set of remaining goods.
        It uses weighted-approval-voting.

        >>> agent1 = BinaryAgent({"x","y"})
        >>> agent2 = BinaryAgent({"z","w"})
        >>> fairness_1_of_best_2 = lambda r: 1 if r>=2 else 0
        >>> family = BinaryFamily([agent1,agent2], fairness_1_of_best_2)
        >>> family.choose_good({"x","y","z"})
        'z'
        """
        map_good_to_total_weight = defaultdict(int)
        self.trace("\tCalculating member weights:")
        self.trace("\t\t         \t\tDesired set\t\tr\ts\tWeight")
        for member in self.members:
            member_remaining_value  = member.value(remaining_goods)       # the "r" of the member
            member_current_value    = member.value(self.allocated_goods)
            member_should_get_value = member.target_value - member_current_value            # the "s" of the member
            member_weight           = weight(member_remaining_value, member_should_get_value)
            self.trace("\t\t{} members\t\t{}\t\t{}\t{}\t{}".format(member.cardinality, member.desired_goods, member_remaining_value, member_should_get_value, member_weight))
            for good in member.desired_goods:
                map_good_to_total_weight[good] += member_weight * member.cardinality

        self.trace("\tCalculating remaining good weights:")
        self.trace("\t\t \tWeight")
        for good in remaining_goods:
            self.trace("\t\t{}\t{}".format(good, map_good_to_total_weight[good]))

        return max(remaining_goods, key=lambda good: map_good_to_total_weight[good])


    def __repr__(self):
        return ", ".join([member.__repr__() for member in self.members])


def allocate(family1: BinaryFamily, family2: BinaryFamily, goods: set):
    """
    Run the RWAV protocol on the two given families.
    Set family1.allocated_goods and family2.allocated_goods to their final bundles.

    >>> fairness_1_of_best_2 = lambda r: 1 if r>=2 else 0
    >>> family1 = BinaryFamily([BinaryAgent({"w","x"},1),BinaryAgent({"x","y"},2),BinaryAgent({"y","z"},3), BinaryAgent({"z","w"},4)], fairness_1_of_best_2)
    >>> family2 = BinaryFamily([BinaryAgent({"w","z"},2),BinaryAgent({"z","y"},3)], fairness_1_of_best_2)
    >>> allocate(family1, family2, ["w","x","y","z"])
    >>> sorted(family1.allocated_goods)
    ['x', 'z']
    >>> sorted(family2.allocated_goods)
    ['w', 'y']
    """

    family1.discard_goods()
    family2.discard_goods()
    remaining_goods=set(goods)

    while True:
        if len(remaining_goods) == 0: break
        allocate.trace("\nFamily 1 chooses a good from {}:".format(remaining_goods))
        g = family1.choose_good(remaining_goods)
        allocate.trace("Family 1 chooses "+g)
        family1.take_good(g)
        remaining_goods.remove(g)
        if len(remaining_goods) == 0: break
        allocate.trace("\nFamily 2 chooses a good from {}:".format(remaining_goods))
        g = family2.choose_good(remaining_goods)
        allocate.trace("Family 2 chooses "+g)
        family2.take_good(g)
        remaining_goods.remove(g)

    allocate.trace("\nFinal allocation: family 1 gets {}, family 2 gets {}".format(
    family1.allocated_goods, family2.allocated_goods))

allocate.trace = lambda *x: None  # To enable tracing, set allocate.trace=True




if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
