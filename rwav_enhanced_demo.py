#!python3

"""
Demonstration of the RWAV and enhanced RWAV protocols.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import binary_families, fairness_criteria
from agents import BinaryAgent
from binary_families import *

if __name__ == "__main__":

    # Define fairness criteria:
    fairness_1_of_best_2 = fairness_criteria.one_of_best_c(2)
    binary_families.allocate_using_enhanced_RWAV.trace = print
    binary_families.allocate_using_RWAV.trace = print

    # Define families:
    family1 = BinaryFamily([
        BinaryAgent("vw",3),
        BinaryAgent("vx",3),
        BinaryAgent("vy",2),
        BinaryAgent("vz",2)], fairness_1_of_best_2, name="Group 1")
    print("{} has:\n{}".format(family1.name,family1))
    family2 = BinaryFamily(
        [BinaryAgent(goods, 1) for goods in ["vw","vx","vy","vz","wx","wy","wz","xy","xz","yz"]],
        fairness_1_of_best_2, name="Group 2")
    print("{} has:\n{}".format(family2.name,family2))


    # Run the protocol:
    binary_families.allocate_using_RWAV.trace = print
    print("\n\nRWAV protocol - group 1 plays first:")
    binary_families.demo(allocate_using_RWAV, [family1, family2], "vwxyz")

    print("\n\nRWAV protocol - group 1 and group 2 exchange roles:")
    binary_families.demo(allocate_using_RWAV, [family2, family1], "vwxyz")

    threshold=0.6
    print("\n\nEnhanced RWAV protocol with threshold {}:".format(threshold))
    binary_families.demo(allocate_using_enhanced_RWAV, [family1, family2], "vwxyz", threshold)
