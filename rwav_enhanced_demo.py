#!python3

"""
Demonstration of the RWAV and enhanced RWAV protocols.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import rwav, fairness_criteria
from agents import BinaryAgent
from rwav import BinaryFamily

if __name__ == "__main__":

    # Define fairness criteria:
    fairness_1_of_best_2 = fairness_criteria.one_of_best_c(2)
    rwav.allocate_enhanced.trace = print

    # Define families:
    family1 = BinaryFamily([
        BinaryAgent("vw",3),
        BinaryAgent("vx",3),
        BinaryAgent("vy",2),
        BinaryAgent("vz",2)], fairness_1_of_best_2)
    family1.trace = print
    print("Group 1 has:\n{}".format(family1))
    family2 = BinaryFamily(
        [BinaryAgent(goods, 1) for goods in ["vw","vx","vy","vz","wx","wy","wz","xy","xz","yz"]],
        fairness_1_of_best_2)
    family2.trace = print
    print("Group 2 has:\n{}".format(family2))


    # Run the protocol:
    rwav.allocate.trace = print
    print("\nRWAV protocol - group 1 plays first:")
    rwav.demo(rwav.allocate, [family1, family2], "vwxyz")

    print("\nRWAV protocol - group 1 and group 2 exchange roles:")
    rwav.demo(rwav.allocate, [family2, family1], "vwxyz")

    threshold=0.6
    print("\nEnhanced RWAV protocol with threshold {}:".format(threshold))
    rwav.demo(rwav.allocate_enhanced, [family2, family1], "vwxyz", threshold)
