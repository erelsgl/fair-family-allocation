#!python3

"""
Defines agents with general, additive and binary preferences.
"""

import abc


def plural(i: int)->str:
    return " " if i==1 else "s"


class Agent(metaclass=abc.ABCMeta):
    """
    Represents an agent or several agents with an abstract valuation function.
    """

    def __init__(self, total_value:float, cardinality:int=1):
        self.the_total_value = total_value
        self.cardinality = cardinality

    @abc.abstractmethod
    def value(self, goods:set)->int:
        """
        Calculates the agent's value for the given set of goods.
        """

    def total_value(self):
        """
        Calculates the agent's value for the entire set of goods.
        """
        return self.the_total_value



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

    def total_value(self):
        """
        Calculates the agent's value for the entire set of goods.
        """
        return self.the_total_value

    def __repr__(self):
        return "{} agent{} with monotone valuations".format(self.cardinality, plural(self.cardinality))


class BinaryAgent(Agent):
    """
    Represents an agent with binary valuations, or several agents with the same binary valuations.

    >>> BinaryAgent({"x","y","z"})
    1 agent  who want ['x', 'y', 'z']
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

    def total_value(self):
        return self.the_total_value

    def __repr__(self):
        return "{} agent{} who want {}".format(self.cardinality, plural(self.cardinality), sorted(self.desired_goods))



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
