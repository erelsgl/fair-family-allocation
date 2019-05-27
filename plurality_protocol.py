#!python3

"""
A partial implementation of the plurality-protocol for k families\ with monotone valuations.

See: https://arxiv.org/abs/1709.02564 Theorem 5.5 for details.
"""

from agents import *
from families import Family
import fairness_criteria
import itertools
    


trace = lambda *x: None  # To enable tracing, set trace=print


def best_index_by_plurality(family:Family, partition:list) -> int:
    """
    Returns the index of the bundle that is most-valuable for a plurality of the members of the given family.
    :param   family: a Family object, with several members.
    :param   partition: a list of some k bundles.
    :return: an index in [0,..,k-1] that points to a bundle whose value is largest for the largest number of members.
    If there are two or more such bundles, the first index is returned.

    >>> family1 = Family([BinaryAgent("xy",1), BinaryAgent("yz",2)], fairness_criteria.OneOfBestC(2), name="Family 1")
    >>> best_index_by_plurality(family1, ["xy","yz"])
    1
    """
    votes = [0] * len(partition)
    for member in family.members:
        best = member.best_index(partition)
        votes[best] += member.cardinality
    winner = max(range(len(partition)), key=lambda i: votes[i])
    trace("{}: votes={}, winner=allocation[{}]={}".format(family.name, votes, winner, partition[winner]))
    return winner


def find_plurality_envy_free_allocation(families: list, partition:list) -> bool:
    """
    Find a permutation of the given partition in which
    each family prefers (by a plurality voting) a different bundle.
    :param families: a list of k Family objects.
    :param partition: a list of k sets of items.
    :return: a permutation of partition such that families[i] prefers permutation[i].
    If no such permutation exists, returns None.

    >>> family1 = Family([BinaryAgent("wx",1), BinaryAgent("wxy",1), BinaryAgent("yz",1)], fairness_criteria.OneOfBestC(2), name="Family 1")
    >>> family2 = Family([BinaryAgent("wx",1), BinaryAgent("xyz",1), BinaryAgent("yz",1)], fairness_criteria.OneOfBestC(2), name="Family 2")
    >>> partition = [set("wx"),set("yz")]
    >>> alloc = find_plurality_envy_free_allocation([family1,family2], partition)
    >>> sorted(alloc[0]), sorted(alloc[1])
    (['w', 'x'], ['y', 'z'])
    >>> alloc = find_plurality_envy_free_allocation([family2,family1], partition)
    >>> sorted(alloc[0]), sorted(alloc[1])
    (['y', 'z'], ['w', 'x'])
    >>> find_plurality_envy_free_allocation([family1,family1], partition) is None
    True
    """
    allocation = [None]*len(families)
    best_indices = set()
    for i in range(len(families)):
        family = families[i]
        i_best = best_index_by_plurality(family, partition)
        if i_best in best_indices:
            trace("Two families vote for {} - no permutation is plurality-EF")
            return None
        best_indices.add(i_best)
        allocation[i] = partition[i_best]
    return allocation


def find_plurality_EF2_allocation(families: list, subsimplex_vertices: list) -> bool:
    """
    Find an allocation which is envy-free-up-to-2 for a plurality of members in each family.
    :param families: a list of k Family objects.
    :param subsimplex_vertices: a list of k "vertices". Each vertex is a partial-partition - a list of k sets of items.
    :return:

    >>> family1 = Family([BinaryAgent("wx",1), BinaryAgent("wyz",1), BinaryAgent("yz",1)], fairness_criteria.OneOfBestC(2), name="Family 1")
    >>> family2 = Family([BinaryAgent("wx",1), BinaryAgent("xy",1), BinaryAgent("yz",1)], fairness_criteria.OneOfBestC(2), name="Family 2")
    >>> partition1 = [set("w"),set("yz")]
    >>> partition2 = [set("wx"),set("z")]
    >>> alloc = find_plurality_EF2_allocation([family1,family2], [partition1,partition2])
    >>> sorted(alloc[0]), sorted(alloc[1])
    (['y', 'z'], ['w', 'x'])
    >>> alloc = find_plurality_EF2_allocation([family2,family1], [partition1,partition2])
    >>> sorted(alloc[0]), sorted(alloc[1])
    (['y', 'z'], ['w', 'x'])
    >>> alloc = find_plurality_EF2_allocation([family1,family2], [partition2,partition1])
    >>> sorted(alloc[0]), sorted(alloc[1])
    (['w', 'x'], ['y', 'z'])
    """
    map_family_index_to_best_index = [None]*len(families)
    best_indices = set()
    for i in range(len(families)):
        family = families[i]
        partition = subsimplex_vertices[i]
        i_best = best_index_by_plurality(family, partition)
        if i_best in best_indices:
            trace("Two families vote for {} - no permutation is plurality-EF")
            return None
        best_indices.add(i_best)
        map_family_index_to_best_index[i] = i_best

    # Create the allocation:
    allocation = [None]*len(families)
    for i in range(len(families)):
        i_best = map_family_index_to_best_index[i]
        allocation[i] = set()
        for partition in subsimplex_vertices:
            allocation[i].update(partition[i_best])

    return allocation





if __name__ == "__main__":
    import doctest
    # trace = print
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
