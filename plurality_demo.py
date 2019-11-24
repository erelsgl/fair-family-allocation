#!python3

"""
Demonstration of a plurality-voting in an approximately-EF protocol.

See: https://arxiv.org/abs/1709.02564 Theorem 5.5 for details.
"""

from agents import *
from families import Family
import fairness_criteria
import plurality_protocol, logging

def make_family_12_goods(valuation_lists:list, name:str):
    """
    A helper routine for creating families for the present demo only.
    Create a family with agents with additive valutaions over the 12 goods a,b,c,d,e,f,g,h,i,j,k,l.
    :param valuation_lists: contains n lists; each list should contain 12 values.
    :return: a family with n additive agents.

    >> make_family_12_goods([[1,1,1,1,2,2,2,2,3,3,3,3],[4,4,4,5,5,5,6,6,6,7,7,7]], "Test family")
    Test family seeks envy-free-except-2 and has:
     * 1 agent  with additive valuations: a=1 b=1 c=1 d=1 e=2 f=2 g=2 h=2 i=3 j=3 k=3 l=3
     * 1 agent  with additive valuations: a=4 b=4 c=4 d=5 e=5 f=5 g=6 h=6 i=6 j=7 k=7 l=7
    """
    members = []
    EF2  = fairness_criteria.EnvyFreeExceptC(c=2)
    for valuation_list in valuation_lists:
        valuation = {
            'a': valuation_list[0],
            'b': valuation_list[1],
            'c': valuation_list[2],
            'd': valuation_list[3],
            'e': valuation_list[4],
            'f': valuation_list[5],
            'g': valuation_list[6],
            'h': valuation_list[7],
            'i': valuation_list[8],
            'j': valuation_list[9],
            'k': valuation_list[10],
            'l': valuation_list[11],
        }
        members.append(AdditiveAgent(valuation, cardinality=1))
    return Family(members, EF2, name=name)


if __name__ == "__main__":
    plurality_protocol.logger.setLevel(logging.INFO)

    families = [
        make_family_12_goods([
            [1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1],
        ], "Group 1"),
        make_family_12_goods([
            [1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2],
            [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1],
        ], "Group 2"),
        make_family_12_goods([
            [1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
            [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3],
            [1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1],
        ], "Group 3"),
        make_family_12_goods([
            [1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3],
            [1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1],
        ], "Group 4"),
    ]

    subsimplex_vertices    = [
        ["abc","def","ghi","kl"],
        ["abc","ef","ghi","kl"],
        ["abc","ef","hi","kl"],
        ["abc","ef","hij","kl"]]

    print("Subsimplex vertices:",subsimplex_vertices)
    allocation = plurality_protocol.find_plurality_EF2_allocation(families, subsimplex_vertices)

    print("\nFinal allocation:")
    for index in range(len(families)):
        print (" * ", families[index].allocation_description(allocation[index], allocation))
