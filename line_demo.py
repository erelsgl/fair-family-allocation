#!python3

"""
Demonstration of the line protocol.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import line_protocol
from agents import BinaryAgent
from families import Family
from utils import demo



if __name__ == "__main__":

    # Define fairness criteria:
    line_protocol.allocate.trace = print
    goods = "vwxyz"

    family1 = Family([
        BinaryAgent("wx",2),
        BinaryAgent("xy",1),
        BinaryAgent("yz",5),
        BinaryAgent("zw",3)], name="Group 1")
    family2 = Family([
        BinaryAgent("wz",2),
        BinaryAgent("zy",3)], name="Group 2")
    family3 = Family([
        BinaryAgent("vw",3),
        BinaryAgent("vx",3),
        BinaryAgent("vy",2),
        BinaryAgent("vz",2)], name="Group 3")
    demo(line_protocol.allocate, [family1, family2], "wxyz")
    print("\n\n\n")
    demo(line_protocol.allocate, [family1, family3], "vwxyz")
    print("\n\n\n")
    demo(line_protocol.allocate, [family2, family3], "zyxwv")
