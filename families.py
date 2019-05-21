#!python3

"""
Classes that represent families (groups) of agents.
"""


from agents import *

class Family:
    """
    Represents a group of agents.
    """
    def __init__(self, members:list, fairness_criterion=None, name:str="Anonymous Family"):
        """
        Initialize a family with the given list of agents.
        :param members: a list of Agent objects.
        :param name: the family name, for display purposes.
        """
        self.members = list(members)
        self.fairness_criterion = fairness_criterion
        self.name = name
        self.num_of_members = sum([member.cardinality for member in self.members])

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
            member.is_happy(set(bundle), all_bundles))

    def allocation_description(self, bundle:set, all_bundles:list)->str:
        return "{}: allocated bundle = {}, happy members = {}/{}".format(
            self.name, bundle, self.num_of_happy_members(bundle, all_bundles), self.num_of_members)

    def __repr__(self):
        return self.name + " has:\n"+"\n".join([" * "+member.__repr__() for member in self.members])



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
