#!python3

"""
Demonstration of the RWAV protocol - Round-Robin with Approval Voting - for two families.

See: https://arxiv.org/abs/1709.02564 subsection 3.2 for details.
"""

import fairness_criteria, rwav_protocol
from agents import BinaryAgent
from families import Family
from utils import demo

if __name__ == "__main__":
    rwav_protocol.trace = print
    rwav_protocol.choose_good.trace = print
    rwav_protocol.member_weight.trace = print

    # define fairness criteria:
    fairness_1_of_2_mms  = fairness_criteria.MaximinShareOneOfC(2)
    fairness_1_of_best_2 = fairness_criteria.OneOfBestC(2)

    # Define families:
    family1 = Family([
        BinaryAgent("vx",2),
        BinaryAgent("vxy",1),
        BinaryAgent("wxyz",5),
        BinaryAgent("zw",3)], fairness_1_of_2_mms, name="Group 1")
    family2 = Family([
        BinaryAgent("wxyz",2),
        BinaryAgent("vz",3)], fairness_1_of_best_2, name="Group 2")

    # Run the protocol:
    print("\n\n\nRWAV protocol - {} plays first".format(family1.name))
    demo(rwav_protocol.allocate, [family1, family2], "vwxyz")

    print("\n\n\nRWAV protocol - {} plays first".format(family2.name))
    demo(rwav_protocol.allocate, [family2, family1], "vwxyz")

