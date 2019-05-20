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
    rwav.allocate.trace = print
    rwav.choose_good.trace = print
    rwav.member_weight.trace = print

    # Define families:
    family1 = BinaryFamily([
        BinaryAgent("vx",2),
        BinaryAgent("vxy",1),
        BinaryAgent("wxyz",5),
        BinaryAgent("zw",3)], fairness_1_of_2_mms, name="Group 1")
    print("{} has:\n{}".format(family1.name, family1))
    family2 = BinaryFamily([
        BinaryAgent("wxyz",2),
        BinaryAgent("vz",3)], fairness_1_of_2_mms, name="Group 2")
    print("{} has:\n{}".format(family2.name, family2))

    # Run the protocol:
    print("\n\nRWAV protocol - {} plays first".format(family1.name))
    rwav.demo(rwav.allocate, [family1, family2], "wxyz")

    print("\n\nRWAV protocol - {} plays first".format(family2.name))
    rwav.demo(rwav.allocate, [family2, family1], "wxyz")

