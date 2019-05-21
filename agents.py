#!python3

"""
Classes that represent agents with general, additive and binary preferences.
"""


import abc  # abstract classes
from utils import plural


class Agent(metaclass=abc.ABCMeta):
    """
    An abstract class.
    Represents an agent or several agents with the same valuation function.
    """

    def __init__(self, total_value:float, cardinality:int=1):
        self.total_value = total_value
        self.cardinality = cardinality

    @abc.abstractmethod
    def value(self, bundle:set)->int:
        """
        Abstract method: - to be overridden in sub-classes.
                 Should calculate the agent's value for the given bundle of goods.
        """

    def value_except_best_good(self, bundle:set)->int:
        """
        Calculates the value of the given bundle when the "best" good is removed from it.
        Formally, it calculates:
              min [g in bundle] value (bundle - g)
        This is a subroutine in checking whether an allocation is EF1.
        """
        if len(bundle)==0: return 0
        else: return min([
            self.value(bundle.difference(set(good)))
            for good in bundle
        ])

    def value_except_worst_good(self, bundle:set)->int:
        """
        Calculates the value of the given bundle when the "worst" good is removed from it.
        Formally, it calculates:
              max [g in bundle] value (bundle - g)
        This is a subroutine in checking whether an allocation is EFx.
        """
        if len(bundle)==0: return 0
        else: return max([
            self.value(bundle.difference(set(good)))
            for good in bundle
        ])

    def is_EF1(self, own_bundle: set, all_bundles: list)->bool:
        """
        Checks whether the current agent finds the given allocation EF1.
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EF1.
        """
        own_value = self.value(own_bundle)
        for other_bundle in all_bundles:
            if own_value < self.value_except_best_good(other_bundle):
                return False
        return True

    def is_EFx(self, own_bundle: set, all_bundles: list)->bool:
        """
        Checks whether the current agent finds the given allocation EFx.
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EFx.
        """
        own_value = self.value(own_bundle)
        for other_bundle in all_bundles:
            if own_value < self.value_except_worst_good(other_bundle):
                return False
        return True

    def is_EF(self, own_bundle: set, all_bundles: list)->bool:
        """
        Checks whether the current agent finds the given allocation envy-free.
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation envy-free.
        """
        own_value = self.value(own_bundle)
        for other_bundle in all_bundles:
            if own_value < self.value(other_bundle):
                return False
        return True


class MonotoneAgent(Agent):
    """
    Represents an agent or several agents with a general monotone valuation function.

    >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
    >>> a
    1 agent  with monotone valuations
    >>> a.value("")
    0
    >>> a.value({"x"})
    1
    >>> a.value("yx")
    4
    >>> a.value({"y","x"})
    4
    >>> a.is_EF({"x"}, [{"y"}])
    False
    >>> a.is_EF1({"x"}, [{"y"}])
    True
    >>> a.is_EFx({"x"}, [{"y"}])
    True
    >>> MonotoneAgent({"x": 1, "y": 2, "xy": 4}, cardinality=2)
    2 agents with monotone valuations

    """
    def __init__(self, map_bundle_to_value:dict, cardinality:int=1):
        """
        Initializes an agent with a given valuation function.
        :param map_bundle_to_value: a dict that maps each subset of goods to its value.
        :param cardinality: the number of agents with the same set of desired goods.
        """
        total_value = max(map_bundle_to_value.values())
            # The valuation is assumed to be monotone,
            # so we assume that the total value is the maximum value.
        super().__init__(total_value=total_value, cardinality=cardinality)
        self.map_bundle_to_value = {frozenset(bundle):value for bundle,value in  map_bundle_to_value.items()}
        self.map_bundle_to_value[frozenset()] = 0   # normalization: the value of the empty bundle is always 0

    def value(self, goods:set)->int:
        """
        Calculates the agent's value for the given set of goods.
        """
        goods = frozenset(goods)
        if goods in self.map_bundle_to_value:
            return self.map_bundle_to_value[goods]
        else:
            raise ValueError("The value of {} is not specified in the valuation function".format(goods))

    def __repr__(self):
        return "{} agent{} with monotone valuations".format(self.cardinality, plural(self.cardinality))


class BinaryAgent(Agent):
    """
    Represents an agent with binary valuations, or several agents with the same binary valuations.

    >>> a = BinaryAgent({"x","y","z"})
    >>> a
    1 agent  who want ['x', 'y', 'z']
    >>> a.value({"x","w"})
    1
    >>> a.value({"y","z"})
    2
    >>> a.is_EF({"x","w"},[{"y","z"}])
    False
    >>> a.is_EF1({"x","w"},[{"y","z"}])
    True
    >>> a.is_EF1({"v","w"},[{"y","z"}])
    False
    >>> a.is_EF1(set(),[{"y","w"}])
    True
    >>> a.is_EF1(set(),[{"y","z"}])
    False
    >>> BinaryAgent({"x","y","z"}, 2)
    2 agents who want ['x', 'y', 'z']
    """

    def __init__(self, desired_goods:set, cardinality:int=1):
        """
        Initializes an agent with a given set of desired goods.
        :param desired_goods: a set of strings - each string is a good.
        :param cardinality: the number of agents with the same set of desired goods.
        """
        super().__init__(total_value=len(desired_goods), cardinality=cardinality)
        self.desired_goods = set(desired_goods)

    def value(self, goods:set)->int:
        """
        Calculates the agent's value for the given set of goods.

        >>> BinaryAgent({"x","y","z"}).value({"w","x","y"})
        2
        >>> BinaryAgent({"x","y","z"}).value({"x","y"})
        2
        >>> BinaryAgent({"x","y","z"}).value("y")
        1
        >>> BinaryAgent({"x","y","z"}).value({"w"})
        0
        >>> BinaryAgent({"x","y","z"}).value(set())
        0
        >>> BinaryAgent(set()).value({"x","y","z"})
        0
        """
        # if isinstance(goods,set):
        goods = set(goods)
        return len(self.desired_goods.intersection(goods))
        # else:
        #     raise ValueError("goods must be a set")

    def __repr__(self):
        return "{} agent{} who want {}".format(self.cardinality, plural(self.cardinality), sorted(self.desired_goods))



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
