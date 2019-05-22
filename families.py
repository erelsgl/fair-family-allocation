#!python3

"""
Classes that represent families (groups) of agents.
"""


from agents import *
import fairness_criteria
from fairness_criteria import FairnessCriterion

class Family:
    """
    Represents a group of agents.

    >>> family1 = Family([BinaryAgent("xy",1), BinaryAgent("yz",2)], fairness_criteria.OneOfBestC(2), name="Family 1")
    >>> family1
    Family 1 has:
     * 1 agent  who want ['x', 'y']
     * 2 agents who want ['y', 'z']
    >>> family1.num_of_members
    3
    >>> family1.num_of_happy_members(set("xw"),[set("yz")])
    1
    >>> family1.num_of_happy_members(set("zw"),[set("xz")])
    2
    >>> family1.num_of_happy_members(set("y"),[set("xz")])
    3
    >>> family1.allocation_description(set("z"),[set("xz")])
    "Family 1: allocated bundle = {'z'}, happy members = 2/3"

    """
    def __init__(self, members:list, fairness_criterion:FairnessCriterion, name:str="Anonymous Family"):
        """
        Initialize a family with the given list of agents.
        :param members: a list of Agent objects.
        :param fairness_criterion: the criterion by which each family member considers an allocation "fair".
        :param name: the family name, for display purposes.
        """
        self.members = list(members)
        self.fairness_criterion = fairness_criterion
        self.name = name
        self.num_of_members = sum([member.cardinality for member in self.members])
        for member in self.members:
            member.target_value = self.fairness_criterion.target_value_for(member.total_value)

    def num_of_members_with(self, predicate)->int:
        """
        Count the members who satisfy the given predicate.
        """
        return sum([member.cardinality for  member in self.members if predicate(member)])

    def num_of_happy_members(self, bundle:set, all_bundles:list):
        """
        Count the members who are happy (-- feel fair) with the given allocation.
        """
        return self.num_of_members_with(lambda member:
            self.fairness_criterion.is_fair_for(member, set(bundle), all_bundles))

    def allocation_description(self, bundle:set, all_bundles:list)->str:
        return "{}: allocated bundle = {}, happy members = {}/{}".format(
            self.name, bundle, self.num_of_happy_members(bundle, all_bundles), self.num_of_members)

    def __repr__(self):
        return self.name + " has:\n"+"\n".join([" * "+member.__repr__() for member in self.members])



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
