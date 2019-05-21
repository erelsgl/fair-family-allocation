#!python3

"""
Classes that represent families (groups) of agents.
"""


import agents


class Family:
    """
    Represents a group of agents.
    """
    def __init__(self, members:list, name:str="Anonymous Family"):
        """
        Initialize a family with the given list of agents.
        :param members: a list of Agent objects.
        :param name: the family name, for display purposes.
        """
        self.members = list(members)
        self.num_of_members = sum([member.cardinality for member in self.members])
        self.name = name

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




class BinaryFamily(Family):
    """
    Represents a family of binary agents with a specific fairness criterion.

    >>> fairness_1_of_best_2 = lambda r: 1 if r>=2 else 0
    >>> family1 = BinaryFamily([BinaryAgent({"x", "y"}, 2), BinaryAgent({"z", "w"}, 1)], fairness_1_of_best_2, "Family 1")
    >>> family1
    Family 1 has:
     * 2 agents who want ['x', 'y']
     * 1 agent  who want ['w', 'z']
    >>> family1.members[0].is_happy(set("w"), [])
    False
    >>> family1.members[1].is_happy(set("w"), [])
    True
    >>> family1.num_of_happy_members(set("w"), [])
    1
    >>> family1.num_of_happy_members(set("xy"), [])
    2
    >>> family1.num_of_happy_members(set("wx"), [])
    3
    """
    def __init__(self, members:list, fairness_criterion, name:str="Anonymous Binary Family"):
        """
        Initializes a family with the given list of agents.
        :param members: a list of BinaryAgent objects.
        :param fairness_criterion: a function that maps the agent's total value (- number of desired goods)
                                to the agent's target value (- number of desired goods the family should have so that the agent is happy)
        """
        super().__init__(members, name)
        for member in self.members:
            member.target_value = fairness_criterion(member.total_value)
            member.is_happy = lambda bundle,all_bundles,member=member: \
                member.value(bundle) >= member.target_value

