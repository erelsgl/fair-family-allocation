#!python3

"""
Utilities for generating partitions of a given subset.

Basedd on code by alexis, https://stackoverflow.com/a/30134039/827927
"""


def partitions(collection:set):
    """
    Generates all partitions of the given set.

    >>> list(partitions([1,2,3]))
    [[[1, 2, 3]], [[1], [2, 3]], [[1, 2], [3]], [[2], [1, 3]], [[1], [2], [3]]]
    """
    if len(collection) == 1:
        yield [ collection ]
        return
    first = collection[0]
    for smaller in partitions(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset
        yield [ [ first ] ] + smaller


def partitions_to_at_most_c(collection:list, c:int):
    """
    Generates all partitions of the given set whose size is at most c.

    >>> list(partitions_to_at_most_c([1,2,3], 2))
    [[[1, 2, 3]], [[1], [2, 3]], [[1, 2], [3]], [[2], [1, 3]]]
    """
    if len(collection) == 1:
        yield [ collection ]
        return
    first = collection[0]
    for smaller in partitions(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset
        if len(smaller)<c:
            yield [ [ first ] ] + smaller


def partitions_to_exactly_c(collection: set, c: int):
    """
    Generates all partitions of the given set whose size is exactly c.

    >>> list(partitions_to_exactly_c([1,2,3], 2))
    [[[1], [2, 3]], [[1, 2], [3]], [[2], [1, 3]]]
    """
    for p in partitions_to_at_most_c(collection, c):
        if len(p)==c:
            yield p


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
