#!python3

"""
Demonstration of the RWAV and enhanced RWAV protocols.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import fairness_criteria, enhanced_rwav_protocol, rwav_protocol
from agents import BinaryAgent
from families import Family
from utils import demo

if __name__ == "__main__":

    # Define fairness criteria:
    fairness_1_of_best_2 = fairness_criteria.OneOfBestC(2)
    enhanced_rwav_protocol.allocate.trace = print
    rwav_protocol.allocate.trace = print

    # Define families:
    family1 = Family([
        BinaryAgent("vw",3),
        BinaryAgent("vx",3),
        BinaryAgent("vy",2),
        BinaryAgent("vz",2)], fairness_1_of_best_2, name="Group 1")
    print(family1)
    family2 = Family(
        [BinaryAgent(goods, 1) for goods in ["vw","vx","vy","vz","wx","wy","wz","xy","xz","yz"]],
        fairness_1_of_best_2, name="Group 2")
    print(family2)


    # Run the protocol:
    rwav_protocol.allocate.trace = print
    print("\n\nRWAV protocol - group 1 plays first:")
    demo(rwav_protocol.allocate, [family1, family2], "vwxyz")

    print("\n\nRWAV protocol - group 1 and group 2 exchange roles:")
    demo(rwav_protocol.allocate, [family2, family1], "vwxyz")

    threshold=0.6
    print("\n\nEnhanced RWAV protocol with threshold {}:".format(threshold))
    demo(enhanced_rwav_protocol.allocate, [family1, family2], "vwxyz", threshold)
