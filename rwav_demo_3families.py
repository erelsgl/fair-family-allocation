#!python3

"""
Demonstration of the RWAV protocol - Round-Robin with Approval Voting - for two families.

See: https://arxiv.org/abs/1709.02564 subsection 5.4 for details.
"""

import fairness_criteria, rwav_protocol,  logging
from agents import BinaryAgent
from families import Family
from utils import demo

if __name__ == "__main__":
    rwav_protocol.logger.setLevel(logging.INFO)
    rwav_protocol.choose_good.logger.setLevel(logging.INFO)
    rwav_protocol.member_weight.logger.setLevel(logging.INFO)

    # define fairness criteria:
    fairness_1_of_best_3 = fairness_criteria.OneOfBestC(c=3)

    # Define families:
    family1 = Family([
        BinaryAgent("vx",2),
        BinaryAgent("vxy",1),
        BinaryAgent("wxyz",5),
        BinaryAgent("zwv",3)], fairness_1_of_best_3, name="Group 1")
    family2 = Family([
        BinaryAgent("wxy",2),
        BinaryAgent("vzx",3)], fairness_1_of_best_3, name="Group 2")
    family3 = Family([
        BinaryAgent("xyz",2),
        BinaryAgent("vxz",1),
        BinaryAgent("wxy",3),
        BinaryAgent("vwy",4)
    ], fairness_1_of_best_3, name="Group 3")

    # Run the protocol:
    print("\n\n\nRWAV protocol - {} plays first".format(family1.name))
    demo(rwav_protocol.allocate, [family1, family2, family3], "vwxyz")

    print("\n\n\nRWAV protocol - {} plays first".format(family2.name))
    demo(rwav_protocol.allocate, [family2, family3, family1], "vwxyz")

    print("\n\n\nRWAV protocol - {} plays first".format(family3.name))
    demo(rwav_protocol.allocate, [family3, family1, family2], "vwxyz")
