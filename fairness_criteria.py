#!python3

"""
Defines various useful fairness criteria to use with fair allocation algorithms.
"""

from abc import ABC, abstractmethod        # Abstract Base Class
from agents import Agent, BinaryAgent
import math


class FairnessCriterion(ABC):
    """
    A fairness criterion for a general instance is a function
    that takes an agent and an allocation, and returns True iff
    the allocation is fair for the agent.

    A fairness criterion for a binary instance is an integer function s(r),
    where r is the number of goods that an agent values at 1,
    and s is the number of goods that this agent should receive in order to satisfy the criterion.
    """

    def __init__(self, name:str):
        self.name = name

    @abstractmethod
    def is_fair_for(agent:Agent, own_bundle: set, all_bundles: list)->bool:
        """
        :param agent:       An agent in some family.
        :param own_bundle:  The bundle allocated to the agent's family.
        :param all_bundles: The list of bundles allocated to all families (a list of sets).
        :return: True iff the agent finds the allocation fair, according to the fairness criterion.
        """

    @abstractmethod
    def target_value_for(total_value: int)->int:
        """
        :param total_value:   The total value of all goods, in the eyes of a particular agent.
        :return: The value that this agent should get in order to satisfy the fairness criterion.
        Relevant mainly for binary instances.
        """



class OneOfBestC(FairnessCriterion):

    def __init__(self, c:int):
        super.__init__("one-of-best-{}".format(c))
        self.c = c

    def target_value_for(self, total_value: int)->int:
        return 1 if total_value >= self.c else 0

    def is_fair_for(self, agent:Agent, own_bundle: set, all_bundles: list)->bool:
        return agent.value(own_bundle) >= self.target_value_for(agent.total_value)



class OneOfBestC(FairnessCriterion):
    """
    Returns the fairness criterion "1 out of best c".

    >>> criterion=OneOfBestC(3)
    >>> [criterion.target_value_for(r) for r in range(10)]
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    """

    def __init__(self, c:int):
        super().__init__("one-of-best-{}".format(c))
        self.c = c

    def target_value_for(self, total_value: int)->int:
        return 1 if total_value >= self.c else 0

    def is_fair_for(self, agent:Agent, own_bundle: set, all_bundles: list)->bool:
        return agent.value(own_bundle) >= self.target_value_for(agent.total_value)


class MaximinShareOneOfC(FairnessCriterion):
    """
    Returns the fairness criterion "1 of c maximin-share".

    >>> criterion=MaximinShareOneOfC(3)
    >>> [criterion.target_value_for(r) for r in range(10)]
    [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
    """

    def __init__(self, c:int):
        super().__init__("1-out-of-{}-maximin-share".format(c))
        self.c = c

    def target_value_for(self, total_value: int)->int:
        return math.floor(total_value/self.c)

    def is_fair_for(self, agent:Agent, own_bundle: set, all_bundles: list)->bool:
        return agent.value(own_bundle) >= self.target_value_for(agent.total_value)


class EnvyFreeExceptC(FairnessCriterion):
    """
    Returns the fairness criterion "EFc" (envy-free except c goods).
    Currently, only c=1 is supported.

    >>> criterion=EnvyFreeExceptC(1)
    >>> [criterion.target_value_for(r) for r in range(10)]
    [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    """

    def __init__(self, c:int):
        super().__init__("Envy-free-except-{}".format(c))
        self.c = c

    def target_value_for(self, total_value: int)->int:
        return max(0, math.floor((total_value - self.c + 1)/2))

    def is_fair_for(self, agent:Agent, own_bundle: set, all_bundles: list)->bool:
        if self.c==0:
            return agent.is_EF(own_bundle, all_bundles)
        elif self.c==1:
            return agent.is_EF1(own_bundle, all_bundles)
        else:
            return agent.value(own_bundle) >= self.target_value_for(agent.total_value)



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
