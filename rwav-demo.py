#!python3

"""
Demonstration of the RWAV protocol - Round-Robin with Approval Voting.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import rwav
from rwav import BinaryAgent, BinaryFamily
import math

if __name__ == "__main__":

    # define fairness criteria:
    fairness_1_of_2_mms  = lambda r: math.floor(r/2)
    fairness_1_of_best_2 = lambda r: 1 if r>=2 else 0

    # Define families:
    family1 = BinaryFamily([BinaryAgent({"w","x"},2),BinaryAgent({"x","y"},1),BinaryAgent({"y","z"},5), BinaryAgent({"z","w"},3)], fairness_1_of_best_2)
    family1.trace = print
    print("Family 1 has {}".format(family1))
    family2 = BinaryFamily([BinaryAgent({"w","z"},2),BinaryAgent({"z","y"},3)], fairness_1_of_2_mms)
    family2.trace = print
    print("Family 2 has {}".format(family2))

    # Run the protocol:
    rwav.allocate.trace = print
    rwav.allocate(family1, family2, ["w","x","y","z"])
