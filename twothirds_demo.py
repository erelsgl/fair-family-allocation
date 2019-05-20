#!python3

"""
Demonstration of the two-thirds protocol.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import rwav, fairness_criteria
from agents import BinaryAgent
from rwav import BinaryFamily

def demo(family:BinaryFamily, goods:set):
    print("\n\nThere are two identical groups with:\n{}".format(family))
    rwav.demo(rwav.allocate_twothirds, [family, family], goods)



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
    demo(family1, "wxyz")

    family2 = BinaryFamily([
        BinaryAgent("wz",2),
        BinaryAgent("zy",3)], fairness_1_of_best_2)
    demo(family2, "wxyz")

    family3 = BinaryFamily([
        BinaryAgent("vw",3),
        BinaryAgent("vx",3),
        BinaryAgent("vy",2),
        BinaryAgent("vz",2)], fairness_1_of_best_2)
    demo(family3, "zyxwv")

    # family4 = BinaryFamily(
    #     [BinaryAgent(goods, 1) for goods in ["vw","vx","vy","vz","wx","wy","wz","xy","xz","yz"]],
    #     fairness_1_of_best_2)
    # demo(family4, "zyxwv")

    # family5 = BinaryFamily(
    #     [BinaryAgent(goods, 1) for goods in ["tu","tv","uv",  "tz",  "xy","xz","yz"]],
    #     fairness_1_of_best_2)
    # demo(family5, "tuvxyz")
    # rwav.demo(rwav.allocate_enhanced, [family5,family5], "tuvxyz", 0.6)
    #
    # family6 = BinaryFamily(
    #     [BinaryAgent(goods, 1) for goods in ["vw","vx","vy","vz","vx","vy","wz","xy","xz","yz"]],
    #     fairness_1_of_best_2)
    # demo(family6, "zyxwv")
    # rwav.demo(rwav.allocate, [family6,family6], "zyxwv")
    # rwav.demo(rwav.allocate_enhanced, [family6,family6], "zyxwv", 0.6)
