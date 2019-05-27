#!python3

"""
Classes that represent agents with general, additive and binary preferences.
"""


from abc import ABC, abstractmethod        # Abstract Base Class
from utils import plural
import math, itertools
import partitions


class Agent(ABC):
    """
    An abstract class.
    Represents an agent or several agents with the same valuation function.
    """

    def __init__(self, desired_goods:set, cardinality:int=1):
        """
        :param desired_goods: the set of all goods that are desired by this agent/s.
        :param cardinality: the number of agent/s with the same valuation function.
        """
        self.desired_goods_list = sorted(desired_goods)
        self.desired_goods = set(desired_goods)
        self.total_value = self.value(self.desired_goods)
        self.cardinality = cardinality

    @abstractmethod
    def value(self, bundle:set)->int:
        """
        This abstract method should calculate the agent's value for the given bundle of goods.

        >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
        >>> a.value(set("xy"))
        4
        """

    def best_index(self, partition:list)->int:
        """
        Returns an index of a bundle that is most-valuable for the agent.
        :param   partition: a list of k sets.
        :return: an index in [0,..,k-1] that points to a bundle whose value for the agent is largest.
        If there are two or more best bundles, the first index is returned.

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 3})
        >>> a.best_index(["xy","z"])
        0
        >>> a.best_index(["y","xz"])
        1
        """
        return max(range(len(partition)), key=lambda i:self.value(partition[i]))


    def value_except_best_c_goods(self, bundle:set, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "best" (at most) c goods are removed from it.
        Formally, it calculates:
              min [G subseteq bundle] value (bundle - G)
        where G is a subset of cardinality at most c.
        This is a subroutine in checking whether an allocation is EFc.

        >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
        >>> a.value_except_best_c_goods(set("xy"), c=1)
        1
        >>> a.value_except_best_c_goods(set("xy"), c=2)
        0
        >>> a.value_except_best_c_goods(set("x"), c=1)
        0
        >>> a.value_except_best_c_goods(set(), c=1)
        0
        """
        if len(bundle) <= c: return 0
        else: return min([
            self.value(bundle.difference(sub_bundle))
            for sub_bundle in itertools.combinations(bundle, c)
        ])

    def value_except_worst_c_goods(self, bundle:set, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "worst" c goods are removed from it.
        Formally, it calculates:
              max [G subseteq bundle] value (bundle - G)
        where G is a subset of cardinality at most c.
        This is a subroutine in checking whether an allocation is EFx.

        >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
        >>> a.value_except_worst_c_goods(set("xy"), c=1)
        2
        """
        if len(bundle) <= c: return 0
        else: return max([
            self.value(bundle.difference(sub_bundle))
            for sub_bundle in itertools.combinations(bundle, c)
        ])


    def values_1_of_c_partitions(self, c:int=1):
        """
        Generates the minimum values in all partitions to c bundles.

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0})
        >>> sorted(a.values_1_of_c_partitions(c=2))
        [1, 2, 3]

        """
        for partition in partitions.partitions_to_exactly_c(self.desired_goods_list, c):
            yield min([self.value(bundle) for bundle in partition])


    def value_1_of_c_MMS(self, c:int=1)->int:
        """
        Calculates the value of the 1-out-of-c maximin-share.
        This is a subroutine in checking whether an allocation is MMS.

        >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
        >>> a.value_1_of_c_MMS(c=1)
        4
        >>> a.value_1_of_c_MMS(c=2)
        1
        >>> a.value_1_of_c_MMS(c=3)
        0
        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0})
        >>> a.value_1_of_c_MMS(c=2)
        3
        """
        if c > len(self.desired_goods):
            return 0
        else:
            return max(self.values_1_of_c_partitions(c))

    def is_EFc(self, own_bundle: set, all_bundles: list, c: int) -> bool:
        """
        Checks whether the current agent finds the given allocation envy-free-except-c-goods (EFc).
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EFc.
        """
        own_value = self.value(own_bundle)
        for other_bundle in all_bundles:
            if own_value < self.value_except_best_c_goods(other_bundle, c):
                return False
        return True

    def is_EF1(self, own_bundle: set, all_bundles: list) -> bool:
        """
        Checks whether the current agent finds the given allocation envy-free-except-1-good (EF1).
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EF1.
        """
        return self.is_EFc(own_bundle, all_bundles, c=1)

    def is_EFx(self, own_bundle: set, all_bundles: list)->bool:
        """
        Checks whether the current agent finds the given allocation EFx.
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EFx.
        """
        own_value = self.value(own_bundle)
        for other_bundle in all_bundles:
            if own_value < self.value_except_worst_c_goods(other_bundle, c=1):
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

    def is_1_of_c_MMS(self, own_bundle:set, c:int, approximation_factor:float=1)->bool:
        own_value = self.value(own_bundle)
        target_value = approximation_factor * self.value_1_of_c_MMS(c)
        return own_value >= target_value

    def is_PROP(self, own_bundle:set, num_of_agents:int)->bool:
        """
        Checks whether the current agent finds the given allocation proportional.
        :param own_bundle:     the bundle consumed by the current agent.
        :param num_of_agents:  the total number of agents.
        :return: True iff the current agent finds the allocation PROPc.
        """
        own_value = self.value(own_bundle)
        return own_value*num_of_agents >= self.total_value

    def is_PROPc(self, own_bundle:set, num_of_agents:int, c:int)->bool:
        """
        Checks whether the current agent finds the given allocation PROPc.
        When there are k agents (or families), an allocation is PROPc for an agent
        if his value for his own bundle is at least 1/k of his value for the following bundle:
            [all the goods except the best c].
        :param own_bundle:   the bundle consumed by the current agent.
        :param num_of_agents:  the total number of agents.
        :param c: how many best-goods to exclude from the total bundle.
        :return: True iff the current agent finds the allocation PROPc.
        """
        own_value = self.value(own_bundle)
        total_except_best_c = self.value_except_best_c_goods(
            self.desired_goods, c=num_of_agents-1)
        return own_value*num_of_agents >= total_except_best_c



class MonotoneAgent(Agent):
    """
    Represents an agent or several agents with a general monotone valuation function.

    >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
    >>> a
    1 agent  with monotone valuations. Desired goods: ['x', 'y']
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
    2 agents with monotone valuations. Desired goods: ['x', 'y']

    """
    def __init__(self, map_bundle_to_value:dict, cardinality:int=1):
        """
        Initializes an agent with a given valuation function.
        :param map_bundle_to_value: a dict that maps each subset of goods to its value.
        :param cardinality: the number of agents with the same valuation.
        """
        self.map_bundle_to_value = {frozenset(bundle):value for bundle,value in  map_bundle_to_value.items()}
        self.map_bundle_to_value[frozenset()] = 0   # normalization: the value of the empty bundle is always 0
        desired_goods = max(map_bundle_to_value.keys(), key=lambda k:map_bundle_to_value[k])
        super().__init__(desired_goods, cardinality=cardinality)

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
        return "{} agent{} with monotone valuations. Desired goods: {}".format(self.cardinality, plural(self.cardinality), sorted(self.desired_goods))




class AdditiveAgent(Agent):
    """
    Represents an agent or several agents with an additive valuation function.

    >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0})
    >>> a
    1 agent  with additive valuations: w=0 x=1 y=2 z=4
    >>> a.value(set())
    0
    >>> a.value({"w"})
    0
    >>> a.value({"x"})
    1
    >>> a.value("yx")
    3
    >>> a.value({"y","x","z"})
    7
    >>> a.is_EF({"y"}, [{"y"},{"x"},{"z"},set()])
    False
    >>> a.is_PROP({"y"}, 4)
    True
    >>> a.is_PROP({"y"}, 3)
    False
    >>> a.is_PROPc({"y"}, 3, c=1)
    True
    >>> a.is_EF1({"y"}, [{"x","z"}])
    True
    >>> a.is_EF1({"x"}, [{"y","z"}])
    False
    >>> a.is_EFx({"x"}, [{"y"}])
    True
    >>> a.value_1_of_c_MMS(c=4)
    0
    >>> a.value_1_of_c_MMS(c=3)
    1
    >>> a.value_1_of_c_MMS(c=2)
    3
    >>> AdditiveAgent({"x": 1, "y": 2, "z": 4}, cardinality=2)
    2 agents with additive valuations: x=1 y=2 z=4

    """
    def __init__(self, map_good_to_value:dict, cardinality:int=1):
        """
        Initializes an agent with a given additive valuation function.
        :param map_good_to_value: a dict that maps each single good to its value.
        :param cardinality: the number of agents with the same valuation.
        """
        self.map_good_to_value = map_good_to_value
        desired_goods = set([g for g,v in map_good_to_value.items() if v>0])
        super().__init__(desired_goods, cardinality=cardinality)

    def value(self, goods:set)->int:
        """
        Calculates the agent's value for the given set of goods.
        """
        return sum([self.map_good_to_value[g] for g in goods])

    def value_except_best_c_goods(self, bundle:set, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "best" (at most) c goods are removed from it.
        Formally, it calculates:
              min [G subseteq bundle] value (bundle - G)
        where G is a subset of cardinality at most c.
        This is a subroutine in checking whether an allocation is EFc.

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4})
        >>> a.value_except_best_c_goods(set("xyz"), c=1)
        3
        >>> a.value_except_best_c_goods(set("xyz"), c=2)
        1
        >>> a.value_except_best_c_goods(set("xy"), c=1)
        1
        >>> a.value_except_best_c_goods(set("xy"), c=2)
        0
        >>> a.value_except_best_c_goods(set("x"), c=1)
        0
        >>> a.value_except_best_c_goods(set(), c=1)
        0
        """
        if len(bundle) <= c: return 0
        sorted_bundle = sorted(bundle, key=lambda g: -self.map_good_to_value[g]) # sort the goods from best to worst
        return self.value(sorted_bundle[c:])  # remove the best c goods

    def value_except_worst_c_goods(self, bundle:set, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "worst" c goods are removed from it.
        Formally, it calculates:
              max [G subseteq bundle] value (bundle - G)
        where G is a subset of cardinality at most c.
        This is a subroutine in checking whether an allocation is EFx.

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4})
        >>> a.value_except_worst_c_goods(set("xyz"), c=1)
        6
        >>> a.value_except_worst_c_goods(set("xy"), c=1)
        2
        >>> a.value_except_worst_c_goods(set("xy"), c=2)
        0
        >>> a.value_except_worst_c_goods(set("x"), c=1)
        0
        >>> a.value_except_worst_c_goods(set(), c=1)
        0
        """
        if len(bundle) <= c: return 0
        sorted_bundle = sorted(bundle, key=lambda g: self.map_good_to_value[g])  # sort the goods from worst to best:
        return self.value(sorted_bundle[c:])  # remove the worst c goods

    def __repr__(self):
        vals = " ".join(["{}={}".format(k,v) for k,v in sorted(self.map_good_to_value.items())])
        return "{} agent{} with additive valuations: {}".format(self.cardinality, plural(self.cardinality), vals)



class BinaryAgent(Agent):
    """
    Represents an agent with binary valuations, or several agents with the same binary valuations.

    >>> a = BinaryAgent({"x","y","z"})
    >>> a
    1 binary agent  who want ['x', 'y', 'z']
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
    >>> a.is_1_of_c_MMS({"x","w"}, c=2)
    True
    >>> a.is_1_of_c_MMS({"w"}, c=2)
    False
    >>> BinaryAgent({"x","y","z"}, 2)
    2 binary agents who want ['x', 'y', 'z']
    """

    def __init__(self, desired_goods:set, cardinality:int=1):
        """
        Initializes an agent with a given set of desired goods.
        :param desired_goods: a set of strings - each string is a good.
        :param cardinality: the number of agents with the same set of desired goods.
        """
        super().__init__(desired_goods, cardinality=cardinality)

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

    def value_except_best_c_goods(self, bundle:set, c:int=1)->int:
        if len(bundle) <= c: return 0
        return self.value(bundle) - c

    def value_except_worst_c_goods(self, bundle:set, c:int=1)->int:
        if len(bundle) <= c: return 0
        return self.value(bundle) - c

    def value_1_of_c_MMS(self, c:int=1)->int:
        return math.floor(self.total_value / c)

    def __repr__(self):
        return "{} binary agent{} who want {}".format(self.cardinality, plural(self.cardinality), sorted(self.desired_goods))



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
