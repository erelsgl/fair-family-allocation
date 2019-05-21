#!python3

"""
The line-allocation (1/2-democratic EF1 for two families with general monotone agents).

See: https://arxiv.org/abs/1709.02564 Section 4 for details.
"""

from agents import *
from families import Family



def allocate(families:list, goods: set)->list:
    """
    Order the goods on a line and allocate them in an EF1 way.
    Currently only 2 families are supported.
    :return a list of bundles - a bundle per family.

    >>> family1 = Family([BinaryAgent({"w","x"},1),BinaryAgent({"x","y"},2),BinaryAgent({"y","z"},3), BinaryAgent({"z","w"},4)], name="Family 1")
    >>> family2 = Family([BinaryAgent({"w","z"},2),BinaryAgent({"z","y"},3)], name="Family 2")
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
    if n_families!=2:
        raise("Currently only 2 families are supported")

    # Set the happiness criterion for all agents to EF1:
    for family in families:
        for member in family.members:
            member.is_happy = lambda bundle, all_bundles, member=member: \
                member.is_EF1(bundle, all_bundles)

    goods=list(goods)  # order the goods on a line
    left_bundle = set()
    right_bundle = set(goods)
    bundles = [set(),set()]
    for good in goods:
        left_bundle.add(good)
        right_bundle.remove(good)
        allocate.trace("{} | {}:".format(left_bundle,right_bundle))
        for family_index in range(len(families)):
            family = families[family_index]
            num_of_EF1_members = family.num_of_members_with(
                lambda member: member.is_EF1(left_bundle, [right_bundle]))
            allocate.trace("   {}: {}/{} members think the left bundle is EF1".format(family.name, num_of_EF1_members, family.num_of_members))
            if num_of_EF1_members >= 0.5*family.num_of_members:
                other_family_index = 1 - family_index
                other_family = families[other_family_index]
                allocate.trace("   {} gets the left bundle".format(family.name))
                allocate.trace("   {} gets the right bundle".format(other_family.name))
                bundles[family_index] = left_bundle
                bundles[other_family_index] = right_bundle
                return bundles
    raise AssertionError("The paper proves that the protocol must end with an allocation, but it did not - there must be a bug")

allocate.trace = lambda *x: None  # To enable tracing, set allocate.trace=print






if __name__ == "__main__":
    import doctest
    # allocate.trace = print
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
