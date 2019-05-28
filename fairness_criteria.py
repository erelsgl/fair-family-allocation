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

    def __init__(self, name:str, abbreviation:str):
        self.name = name
        self.abbreviation = abbreviation

    @abstractmethod
    def target_value_for_agent(self, agent:Agent)->int:
        """
        :param agent:   an Agent object.
        :return: The value that this agent should get in order to satisfy the fairness criterion.
        """

    @abstractmethod
    def target_value_for_binary(self, total_value: int)->int:
        """
        :param total_value:   The total value of all goods, in the eyes of a particular agent.
        :return: The value that this agent should get in order to satisfy the fairness criterion.
        Relevant mainly for binary instances.
        """

    def is_fair_for(self, agent:Agent, own_bundle: set, all_bundles: list)->bool:
        """
        The default fairness calculation - checks if the bundle's value is above the agent's target value.
        Relevant for fairness criteria that ignore the other bundles, e.g. proportionality or MMS.
        :param agent:       An agent in some family.
        :param own_bundle:  The bundle allocated to the agent's family.
        :param all_bundles: The list of bundles allocated to all families (a list of sets).
        :return: True iff the agent finds the allocation fair, according to the fairness criterion.
        """
        return agent.value(own_bundle) >= self.target_value_for_agent(agent)


class OneOfBestC(FairnessCriterion):
    """
    Returns the fairness criterion "1 out of best c".

    >>> criterion=OneOfBestC(3)
    >>> [criterion.target_value_for_binary(r) for r in range(10)]
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    """

    def __init__(self, c:int):
        super().__init__("one-of-best-{}".format(c), "1-of-best-{}".format(c))
        self.c = c

    def target_value_for_agent(self, agent: Agent)->int:
        return agent.value_of_cth_best_good(self.c)

    def target_value_for_binary(self, total_value: int)->int:
        return 1 if total_value >= self.c else 0


class MaximinShareOneOfC(FairnessCriterion):
    """
    Returns the fairness criterion "1 of c maximin-share".

    >>> criterion=MaximinShareOneOfC(3)
    >>> [criterion.target_value_for_binary(r) for r in range(10)]
    [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
    """

    def __init__(self, c:int, approximation_factor:float=1):
        if approximation_factor==1:
            name="1-out-of-{}-maximin-share".format(c)
            abbreviation="1-of-{}-MMS".format(c)
        else:
            name="{}-fraction 1-out-of-{}-maximin-share".format(approximation_factor, c)
            abbreviation = "{}-fraction 1-of-{}-MMS".format(approximation_factor, c)
        super().__init__(name, abbreviation)
        self.c = c
        self.approximation_factor = approximation_factor

    def target_value_for_agent(self, agent: Agent)->int:
        return agent.value_1_of_c_MMS(c=self.c, approximation_factor=self.approximation_factor)

    def target_value_for_binary(self, total_value: int)->int:
        return math.floor(total_value/self.c)*self.approximation_factor


class EnvyFreeExceptC(FairnessCriterion):
    """
    Returns the fairness criterion "EFc" (envy-free except c goods).
    Currently, only c=1 is supported.

    >>> criterion=EnvyFreeExceptC(1)
    >>> [criterion.target_value_for_binary(r) for r in range(10)]
    [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    """

    def __init__(self, c:int):
        super().__init__("envy-free-except-{}".format(c), "EF{}".format(c))
        self.c = c

    def target_value_for_agent(self, agent: Agent)->int:
        raise ValueError("target value is not relevant for envy-freeness concepts")

    def target_value_for_binary(self, total_value: int)->int:
        raise ValueError("target value is not relevant for envy-freeness concepts")

    def is_fair_for(self, agent:Agent, own_bundle: set, all_bundles: list)->bool:
        return agent.is_EFc(own_bundle, all_bundles, self.c)


class ProportionalExceptC(FairnessCriterion):
    """
    Returns the fairness criterion "Proportional except c" -
    the agent's value should be at least 1/n times the value of
    the set of all goods minus the c best goods.

    >>> criterion=ProportionalExceptC(num_of_agents=2, c=1)
    >>> [criterion.target_value_for_binary(r) for r in range(10)]
    [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    """

    def __init__(self, num_of_agents:int, c:int):
        super().__init__("proportionality-except-{}".format(c), "PROP-{}".format(c))
        self.c = c
        self.num_of_agents = num_of_agents

    def target_value_for_agent(self, agent: Agent)->int:
        return agent.value_proportional_except_c(num_of_agents=self.num_of_agents, c=self.c)

    def target_value_for_binary(self, total_value: int)->int:
        return max(0, math.ceil((total_value - self.c)/self.num_of_agents))




if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
