#!python3

"""
Demonstration of the line protocol for 2 families.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import line_protocol
from agents import BinaryAgent
from families import Family
from utils import demo
import fairness_criteria


if __name__ == "__main__":
    line_protocol.trace = print

    # Define fairness criteria:
    goods = "vwxyz"

    family1 = Family([
        BinaryAgent("wx",2),
        BinaryAgent("xy",1),
        BinaryAgent("yz",5),
        BinaryAgent("zw",3)], fairness_criteria.EnvyFreeExceptC(1), name="Group 1")
    family2 = Family([
        BinaryAgent("wz",2),
        BinaryAgent("zy",3)], fairness_criteria.EnvyFreeExceptC(1), name="Group 2")
    family3 = Family([
        BinaryAgent("vw",3),
        BinaryAgent("vx",3),
        BinaryAgent("vy",2),
        BinaryAgent("vz",2)], fairness_criteria.EnvyFreeExceptC(1), name="Group 3")

    print("\n\n\ndemocratic-EF1 allocation among two groups:")
    demo(line_protocol.allocate, [family1, family2], "wxyz")
    print("\n\n\n")
    demo(line_protocol.allocate, [family1, family3], "vwxyz")
    print("\n\n\n")
    demo(line_protocol.allocate, [family2, family3], "zyxwv")
