#!python3

"""
Demonstration of the line protocol.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import line_protocol
from agents import *
from families import Family
from utils import demo
import fairness_criteria


if __name__ == "__main__":
    line_protocol.trace = print

    # Define fairness criteria:
    goods = "vwxyz"
    v='v'; w='w'; x='x'; y='y'; z='z'
    k = 3 # num of families

    family1 = Family([
        AdditiveAgent({v:1,w:2,x:4,y:8,z:16}, 5),
        AdditiveAgent({v:16,w:8,x:4,y:2,z:1}, 2)],
        fairness_criteria.MaximinShareOneOfC(c=2*k-1), name="Group 1")
    family2 = Family([
        AdditiveAgent({v:1,w:2,x:4,y:8,z:16}, 5),
        AdditiveAgent({v:16,w:8,x:4,y:2,z:1}, 2)],
        fairness_criteria.MaximinShareOneOfC(c=k, approximation_factor=1/k), name="Group 2")
    family3 = Family([
        BinaryAgent("vw",3),
        BinaryAgent("vx",3),
        BinaryAgent("vy",2),
        BinaryAgent("vz",2)], fairness_criteria.ProportionalExceptC(c=k-1, num_of_agents=k), name="Group 3")

    print("\n\n\ndemocratic-fair allocation among three groups:")
    demo(line_protocol.allocate, [family1, family2, family3], "vwxyz")

