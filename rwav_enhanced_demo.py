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
    rwav.allocate.trace = print

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
    rwav.allocate.trace = print
    print("\n\nRWAV protocol - group 1 plays first:")
    rwav.demo(rwav.allocate, [family1, family2], "vwxyz")

    print("\n\nRWAV protocol - group 1 and group 2 exchange roles:")
    rwav.demo(rwav.allocate, [family2, family1], "vwxyz")

    threshold=0.6
    print("\n\nEnhanced RWAV protocol with threshold {}:".format(threshold))
    rwav.demo(rwav.allocate_enhanced, [family1, family2], "vwxyz", threshold)
