#!python3

"""
The line-allocation (1/2-democratic EF1 for two families with general monotone agents).

See: https://arxiv.org/abs/1709.02564 Theorems 4.2 and 5.8.
"""

from agents import *
from families import Family
import fairness_criteria


trace = lambda *x: None  # To enable tracing, set trace=print


def allocate(families:list, goods:list)->list:
    """
    Order the goods on a line and allocate them in an democratically-fair way.
    :return a list of bundles - a bundle per family.

    >>> fairness_EF1 = fairness_criteria.EnvyFreeExceptC(1)
    >>> family1 = Family([BinaryAgent({"w","x"},1),BinaryAgent({"x","y"},2),BinaryAgent({"y","z"},3), BinaryAgent({"z","w"},4)], fairness_criterion=fairness_EF1, name="Family 1")
    >>> family2 = Family([BinaryAgent({"w","z"},2),BinaryAgent({"z","y"},3)], fairness_criterion=fairness_EF1, name="Family 2")
    >>> (bundle1,bundle2) = allocate([family1, family2], ["w","x","y","z"])
    >>> sorted(bundle1)
    ['w']
    >>> sorted(bundle2)
    ['x', 'y', 'z']
    >>> (bundle1,bundle2) = allocate([family2, family1], ["x","w","y","z"])
    >>> sorted(bundle1)
    ['y', 'z']
    >>> sorted(bundle2)
    ['w', 'x']
    """
    n_families = len(families)
    if n_families==2:
        return _allocate_2(families, goods)
    else:
        return _allocate_k(families, goods)



def _allocate_2(families:list, goods:list)->list:
    """
    An allocation sub-routine for the special case of 2 families.
    Order the goods on a line and allocate them in 1/2-democratic EF1 way among 2 families.
    :return a list of bundles - a bundle per family.
    Based on  https://arxiv.org/abs/1709.02564 Theorem 4.2.

    >>> fairness_EF1 = fairness_criteria.EnvyFreeExceptC(1)
    >>> family1 = Family([BinaryAgent({"w","x"},1),BinaryAgent({"x","y"},2),BinaryAgent({"y","z"},3), BinaryAgent({"z","w"},4)], fairness_criterion=fairness_EF1, name="Family 1")
    >>> family2 = Family([BinaryAgent({"w","z"},2),BinaryAgent({"z","y"},3)], fairness_criterion=fairness_EF1, name="Family 2")
    >>> (bundle1,bundle2) = _allocate_2([family1, family2], ["w","x","y","z"])
    >>> sorted(bundle1)
    ['w']
    >>> sorted(bundle2)
    ['x', 'y', 'z']
    >>> (bundle1,bundle2) = _allocate_2([family2, family1], ["x","w","y","z"])
    >>> sorted(bundle1)
    ['y', 'z']
    >>> sorted(bundle2)
    ['w', 'x']
    """
    k = len(families)   # must be 2
    goods=list(goods)  # order the goods on a line
    left_sequence = list()
    right_sequence = list(goods)
    bundles = [None,None]
    for good in goods:
        trace("\nCurrent partition:  {} | {}:".format(left_sequence,right_sequence))
        left_bundle = set(left_sequence)
        right_bundle = set(right_sequence)
        for family_index in range(len(families)):
            family = families[family_index]
            num_of_happy_members = family.num_of_happy_members(left_bundle, [right_bundle])
            trace("   {}: {}/{} members think the left bundle is {}".format(
                family.name, num_of_happy_members, family.num_of_members, family.fairness_criterion.abbreviation))
            if num_of_happy_members*k >= family.num_of_members:
                other_family_index = 1 - family_index
                other_family = families[other_family_index]
                trace("   {} gets the left bundle".format(family.name))
                trace("   {} gets the right bundle".format(other_family.name))
                bundles[family_index] = left_bundle
                bundles[other_family_index] = right_bundle
                return bundles
        left_sequence.append(good)
        right_sequence.pop(0)
    raise AssertionError(
        "The paper proves that the protocol must end with an allocation, but it did not - there must be a bug")



def _allocate_k(families:list, goods:list)->list:
    """
    An allocation sub-routine for the general case of k families.
    Order the goods on a line and allocate them in 1/k-democratic fair way among k families,
    based on the fairness-criterion of each family.
    :return a list of bundles - a bundle per family.
    Based on  https://arxiv.org/abs/1709.02564 Theorem 5.8.

    >>> fairness_EF1 = fairness_criteria.EnvyFreeExceptC(1)
    >>> family1 = Family([BinaryAgent({"w","x"},1),BinaryAgent({"x","y"},2),BinaryAgent({"y","z"},3), BinaryAgent({"z","w"},4)], fairness_criterion=fairness_EF1, name="Family 1")
    >>> family2 = Family([BinaryAgent({"w","z"},2),BinaryAgent({"z","y"},3)], fairness_criterion=fairness_EF1, name="Family 2")
    >>> (bundle1,bundle2) = _allocate_k([family1, family2], ["w","x","y","z"])
    >>> sorted(bundle1)
    ['w']
    >>> sorted(bundle2)
    ['x', 'y', 'z']
    >>> (bundle1,bundle2) = _allocate_k([family2, family1], ["x","w","y","z"])
    >>> sorted(bundle1)
    ['y', 'z']
    >>> sorted(bundle2)
    ['w', 'x']
    """
    k = len(families)

    if k==1:
        family = families[0]
        trace("   {} gets the remaining bundle".format(family.name))
        return [set(goods)]

    goods=list(goods)  # order the goods on a line
    left_sequence = list()
    right_sequence = list(goods)
    for good in goods:
        trace("\nCurrent partition:  {} | {}:".format(left_sequence,right_sequence))
        left_bundle = set(left_sequence)
        right_bundle = set(right_sequence)
        for family_index in range(len(families)):
            family = families[family_index]
            num_of_happy_members = family.num_of_happy_members(left_bundle, [right_bundle])
            trace("   {}: {}/{} members think the left bundle is {}".format(
                family.name, num_of_happy_members, family.num_of_members, family.fairness_criterion.abbreviation))
            if num_of_happy_members*k >= family.num_of_members:
                trace("   {} gets the left bundle".format(family.name))
                other_families = list(families)
                del other_families[family_index]
                bundles = _allocate_k(other_families, right_sequence)
                bundles.insert (family_index, left_bundle)
                return bundles
        left_sequence.append(good)
        right_sequence.pop(0)
    raise AssertionError(
        "The paper proves that the protocol must end with an allocation, but it did not - there must be a bug")



if __name__ == "__main__":
    import doctest
    # trace = print
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
