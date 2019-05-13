#!python3

"""
Demonstration of the RWAV protocol - Round-Robin with Approval Voting.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import rwav, fairness_criteria
from agents import BinaryAgent
from rwav import BinaryFamily


if __name__ == "__main__":

    # define fairness criteria:
    fairness_1_of_2_mms  = fairness_criteria.maximin_share_one_of_c(2)
    fairness_1_of_best_2 = fairness_criteria.one_of_best_c(2)

    # Define families:
    family1 = BinaryFamily([
        BinaryAgent("wx",2),
        BinaryAgent("xy",1),
        BinaryAgent("yz",5),
        BinaryAgent("zw",3)], fairness_1_of_best_2)
    family1.trace = print
    print("Group 1 has:\n{}".format(family1))
    family2 = BinaryFamily([
        BinaryAgent("wz",2),
        BinaryAgent("zy",3)], fairness_1_of_2_mms)
    family2.trace = print
    print("Group 2 has:\n{}".format(family2))

    # Run the protocol:
    rwav.allocate.trace = print

    print("\n\nRWAV protocol - group 1 plays first")
    rwav.allocate(family1, family2, "wxyz")
    print("Final allocation:\n * Group 1: {}\n * Group 2: {}".format(
    family1.allocation_description(family1.allocated_goods),
    family2.allocation_description(family2.allocated_goods)))

    print("\n\nRWAV protocol - group 2 plays first")
    rwav.allocate(family2, family1, "wxyz")
    print("Final allocation:\n * Group 1: {}\n * Group 2: {}".format(
    family1.allocation_description(family1.allocated_goods),
    family2.allocation_description(family2.allocated_goods)))

