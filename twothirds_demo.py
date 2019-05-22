#!python3

"""
Demonstration of the two-thirds protocol.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import twothirds_protocol, fairness_criteria
from agents import BinaryAgent
from families import Family
import utils
import copy


def demo(family:Family, goods:set):
    family1 = copy.copy(family); family1.name="Group 1"
    family2 = copy.copy(family); family2.name="Group 2"
    print(family1)
    print(family2.name+" is identical.")
    utils.demo(twothirds_protocol.allocate, [family1, family2], goods)



if __name__ == "__main__":

    # Define fairness criteria:
    fairness_1_of_best_2 = fairness_criteria.OneOfBestC(2)
    twothirds_protocol.allocate.trace = print
    goods = "vwxyz"

    family1 = Family([
        BinaryAgent("wx",2),
        BinaryAgent("xy",1),
        BinaryAgent("yz",5),
        BinaryAgent("zw",3)], fairness_1_of_best_2)
    demo(family1, "wxyz")

    family2 = Family([
        BinaryAgent("wz",2),
        BinaryAgent("zy",3)], fairness_1_of_best_2)
    demo(family2, "wxyz")

    family3 = Family([
        BinaryAgent("vw",3),
        BinaryAgent("vx",3),
        BinaryAgent("vy",2),
        BinaryAgent("vz",2)], fairness_1_of_best_2)
    demo(family3, "zyxwv")

    # family4 = Family(
    #     [BinaryAgent(goods, 1) for goods in ["vw","vx","vy","vz","wx","wy","wz","xy","xz","yz"]],
    #     fairness_1_of_best_2)
    # demo(family4, "zyxwv")

    # family5 = Family(
    #     [BinaryAgent(goods, 1) for goods in ["tu","tv","uv",  "tz",  "xy","xz","yz"]],
    #     fairness_1_of_best_2)
    # demo(family5, "tuvxyz")
    # binary_families.demo(binary_families.allocate_using_enhanced_RWAV, [family5,family5], "tuvxyz", 0.6)
    #
    # family6 = Family(
    #     [BinaryAgent(goods, 1) for goods in ["vw","vx","vy","vz","vx","vy","wz","xy","xz","yz"]],
    #     fairness_1_of_best_2)
    # demo(family6, "zyxwv")
    # binary_families.demo(binary_families.allocate_using_RWAV, [family6,family6], "zyxwv")
    # binary_families.demo(binary_families.allocate_using_enhanced_RWAV, [family6,family6], "zyxwv", 0.6)
