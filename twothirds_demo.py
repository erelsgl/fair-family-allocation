#!python3

"""
Demonstration of the two-thirds protocol.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import rwav, fairness_criteria
from agents import BinaryAgent
from rwav import BinaryFamily

def demo(family:BinaryFamily, goods:set):
    print("\nThere are two identical groups with:\n{}".format(family))
    [bundle1,bundle2] = rwav.allocate_twothirds([family, family], goods)
    print("Final allocation:\n * Group 1: {}\n * Group 2: {}".format(
    family.allocation_description(bundle1),
    family.allocation_description(bundle2)))



if __name__ == "__main__":

    # Define fairness criteria:
    fairness_1_of_best_2 = fairness_criteria.one_of_best_c(2)
    rwav.allocate_twothirds.trace = print
    goods = "vwxyz"

    family1 = BinaryFamily([
        BinaryAgent("wx",2),
        BinaryAgent("xy",1),
        BinaryAgent("yz",5),
        BinaryAgent("zw",3)], fairness_1_of_best_2)
    demo(family1, goods)
    family2 = BinaryFamily([
        BinaryAgent("wz",2),
        BinaryAgent("zy",3)], fairness_1_of_best_2)
    demo(family2, goods)
    family3 = BinaryFamily([
        BinaryAgent("vw",3),
        BinaryAgent("vx",3),
        BinaryAgent("vy",2),
        BinaryAgent("vz",2)], fairness_1_of_best_2)
    demo(family3, goods)


