#!python3

"""
Implementation of the RWAV protocol - Round-Robin with Approval Voting.

See: https://arxiv.org/abs/1709.02564 for details.
"""

from functools import lru_cache
from collections import defaultdict
import fairness_criteria
from agents import *


class BinaryFamily:
    """
    Represents a family of binary agents with a specific fairness criterion.

    >>> fairness_1_of_best_2 = lambda r: 1 if r>=2 else 0
    >>> BinaryFamily([BinaryAgent({"x", "y"}, 2), BinaryAgent({"z", "w"}, 1)], fairness_1_of_best_2)
     * 2 agents who want ['x', 'y']
     * 1 agent  who want ['w', 'z']
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

    def num_of_members(self):
        return sum([member.cardinality for  member in self.members])

    def num_of_members_who_want(self, good:str):
        """
        Return the number of family members who want the given good.

        >>> f = BinaryFamily([BinaryAgent({"x", "y"}, 2), BinaryAgent({"y", "z"}, 1)], fairness_criteria.one_of_best_c(2))
        >>> f.num_of_members_who_want("x")
        2
        >>> f.num_of_members_who_want("y")
        3
        >>> f.num_of_members_who_want("z")
        1
        """
        goods = set([good])
        return sum([member.cardinality for  member in self.members if member.value(goods)>0])

    def num_of_happy_members(self, bundle:set):
        """
        Return the number of family members who are "happy" (- feel fair) with the given bundle.

        >>> f = BinaryFamily([BinaryAgent("vwxy", 2), BinaryAgent("yz", 1)], fairness_criteria.maximin_share_one_of_c(2))
        >>> f.num_of_happy_members("x")
        0
        >>> f.num_of_happy_members("y")
        1
        >>> f.num_of_happy_members("z")
        1
        >>> f.num_of_happy_members("wx")
        2
        >>> f.num_of_happy_members("xy")
        3
        """
        bundle = set(bundle)
        return sum([member.cardinality
                    for  member in self.members
                    if member.value(bundle) >= member.target_value])

    def allocation_description(self, bundle:set)->str:
        return "Allocated bundle = {}, happy members = {}/{}".format(
            bundle, self.num_of_happy_members(bundle), self.num_of_members())

    def take_good(self, good:str):
        """
        Add the given good to the family's bundle.
        """
        self.allocated_goods.add(good)

    def take_goods(self, goods:list):
        """
        Add the given goods to the family's bundle.
        """
        for good in goods:
            self.allocated_goods.add(good)

    def discard_goods(self):
        """
        Reset the family's bundle to an empty bundle.
        """
        self.allocated_goods = set()

    def member_weight(self, member:BinaryAgent, remaining_goods:set)->float:
        """
        Calculate the voting-weight of the given member with the given remaining goods.

        >>> Alice = BinaryAgent({"w","x"})
        >>> Bob   = BinaryAgent({"w","x","y","z"})
        >>> fairness_1_of_2_mms = fairness_criteria.maximin_share_one_of_c(2)
        >>> family = BinaryFamily([Alice,Bob], fairness_1_of_2_mms)
        >>> family.member_weight(Alice, {"x","y","z"})
        0.5
        >>> family.member_weight(Bob, {"x","y","z"})
        0.375
        """
        member_remaining_value  = member.value(remaining_goods)               # the "r" of the member
        member_current_value    = member.value(self.allocated_goods)
        member_should_get_value = member.target_value - member_current_value  # the "s" of the member
        member_weight = weight(member_remaining_value, member_should_get_value)
        self.trace("\t\t{} member{}\t\t{}\t\t{}\t{}\t{}".format(
            member.cardinality, plural(member.cardinality),
            sorted(member.desired_goods), member_remaining_value,
            member_should_get_value, member_weight))
        return member_weight

    def choose_good(self, remaining_goods:set)->str:
        """
        Calculate the good that the family chooses from the set of remaining goods.
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
            member_weight           = self.member_weight(member, remaining_goods)
            for good in member.desired_goods:
                map_good_to_total_weight[good] += member_weight * member.cardinality

        self.trace("\tCalculating remaining good weights:")
        self.trace("\t\t \tWeight")
        for good in remaining_goods:
            self.trace("\t\t{}\t{}".format(good, map_good_to_total_weight[good]))

        return min(remaining_goods, key=lambda good: (-map_good_to_total_weight[good], good))




    def __repr__(self):
        return "\n".join([" * "+member.__repr__() for member in self.members])


def allocate(family1: BinaryFamily, family2: BinaryFamily, goods: set):
    """
    Run the RWAV protocol on the two given families.
    Set family1.allocated_goods and family2.allocated_goods to their final bundles.

    >>> fairness_1_of_best_2 = fairness_criteria.one_of_best_c(2)
    >>> family1 = BinaryFamily([BinaryAgent({"w","x"},1),BinaryAgent({"x","y"},2),BinaryAgent({"y","z"},3), BinaryAgent({"z","w"},4)], fairness_1_of_best_2)
    >>> family2 = BinaryFamily([BinaryAgent({"w","z"},2),BinaryAgent({"z","y"},3)], fairness_1_of_best_2)
    >>> allocate(family1, family2, ["w","x","y","z"])
    >>> sorted(family1.allocated_goods)
    ['x', 'z']
    >>> sorted(family2.allocated_goods)
    ['w', 'y']
    """
    remaining_goods=set(goods)
    family1.discard_goods()
    family2.discard_goods()

    turn_index = 0
    while True:
        if len(remaining_goods) == 0: break
        turn_index += 1
        allocate.trace("\nTurn #{}: group 1's turn to pick a good from {}:".format(turn_index, sorted(remaining_goods)))
        g = family1.choose_good(remaining_goods)
        allocate.trace("Group 1 picks "+g)
        family1.take_good(g)
        remaining_goods.remove(g)
        if len(remaining_goods) == 0: break
        turn_index += 1
        allocate.trace("\nTurn #{}: group 2's turn to pick a good from {}:".format(turn_index, sorted(remaining_goods)))
        g = family2.choose_good(remaining_goods)
        allocate.trace("Group 2 picks "+g)
        family2.take_good(g)
        remaining_goods.remove(g)
allocate.trace = lambda *x: None  # To enable tracing, set allocate.trace=True


def allocate_enhanced(family1: BinaryFamily, family2: BinaryFamily, goods: set, threshold: float):
    """
    Run the Enhanced-RWAV protocol (see Section 3 in the paper) on the two given families, with the given threshold.
    Set family1.allocated_goods and family2.allocated_goods to their final bundles.
    :param threshold: a number in [0,1].
      If there is a single good g that is wanted by at least this fraction of members in one of the families,
      then this family gets g and the other family gets the other goods.

    >>> fairness_1_of_best_2 = fairness_criteria.one_of_best_c(2)
    >>> family1 = BinaryFamily([BinaryAgent({"w","x"},1),BinaryAgent({"x","y"},3),BinaryAgent({"y","z"},3), BinaryAgent({"w","v"},3)], fairness_1_of_best_2)
    >>> family2 = BinaryFamily([BinaryAgent({"w","x"},5),BinaryAgent({"y","z"},5)], fairness_1_of_best_2)
    >>> allocate_enhanced(family1, family2, ["v","w","x","y","z"], threshold=0.6)
    >>> sorted(family1.allocated_goods)
    ['y']
    >>> sorted(family2.allocated_goods)
    ['v', 'w', 'x', 'z']
    >>> allocate_enhanced(family2, family1, ["v","w","x","y","z"], threshold=0.6)
    >>> sorted(family1.allocated_goods)
    ['y']
    >>> sorted(family2.allocated_goods)
    ['v', 'w', 'x', 'z']
    """
    family1.discard_goods()
    family2.discard_goods()
    goods = set(goods)

    threshold1 = threshold*family1.num_of_members()
    threshold2 = threshold*family2.num_of_members()
    for g in goods:
        num1 = family1.num_of_members_who_want(g)
        num2 = family2.num_of_members_who_want(g)
        if num1 >= threshold1:
            family1.take_good(g)
            family2.take_goods(goods.difference(set(g)))
            allocate_enhanced.trace("{} out of {} members in group 1 want {}, so group 1 gets {} and group 2 gets the rest".format(
                                     num1,     family1.num_of_members(),     g,                  g))
            return
        elif num2 >= threshold2:
            family2.take_good(g)
            family1.take_goods(goods.difference(set(g)))
            allocate_enhanced.trace("{} out of {} members in group 2 want {}, so group 2 gets {} and group 1 gets the rest".format(
                num2,family2.num_of_members(), g, g))
            return
    allocate(family1, family2, goods)
allocate_enhanced.trace = lambda *x: None  # To enable tracing, set allocate.trace=True






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

@lru_cache(maxsize=None)
def weight(r:int, s:int)->float:
    """
    Calculates the function w(r,s), which represents
       the voting weight of a user with r remaining goods and s missing goods.

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


def plural(i: int)->str:
    return " " if i==1 else "s"


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
