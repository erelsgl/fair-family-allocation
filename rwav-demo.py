#!python3

"""
Demonstration of the RWAV protocol - Round-Robin with Approval Voting.

See: https://arxiv.org/abs/1709.02564 for details.
"""

import rwav
from rwav import BinaryAgent, BinaryFamily
import math

if __name__ == "__main__":

    # define fairness criteria:
    fairness_1_of_2_mms  = lambda r: math.floor(r/2)
    fairness_1_of_best_2 = lambda r: 1 if r>=2 else 0

    # Demonstrate allocate
    fairness_1_of_best_2 = lambda r: 1 if r>=2 else 0
    family1 = BinaryFamily([BinaryAgent({"w","x"},2),BinaryAgent({"x","y"},1),BinaryAgent({"y","z"},5), BinaryAgent({"z","w"},3)], fairness_1_of_best_2)
    family1.trace = print
    family2 = BinaryFamily([BinaryAgent({"w","z"},2),BinaryAgent({"z","y"},3)], fairness_1_of_best_2)
    family2.trace = print
    rwav.allocate.trace = print
    rwav.allocate(family1, family2, ["w","x","y","z"])

    """
    Sample output:

    Family 1 chooses a good from {'y', 'w', 'x', 'z'}:
        Calculating member weights:
                            Desired set		r	s	Weight
            2 members		{'w', 'x'}		2	1	0.25
            1 members		{'y', 'x'}		2	1	0.25
            5 members		{'y', 'z'}		2	1	0.25
            3 members		{'w', 'z'}		2	1	0.25
        Calculating remaining good weights:
                Weight
            y	1.5
            w	1.25
            x	0.75
            z	2.0
    Family 1 chooses z
    
    Family 2 chooses a good from {'y', 'w', 'x'}:
        Calculating member weights:
                            Desired set		r	s	Weight
            2 members		{'w', 'z'}		1	1	0.5
            3 members		{'y', 'z'}		1	1	0.5
        Calculating remaining good weights:
                Weight
            y	1.5
            w	1.0
            x	0
    Family 2 chooses y
    
    Family 1 chooses a good from {'w', 'x'}:
        Calculating member weights:
                            Desired set		r	s	Weight
            2 members		{'w', 'x'}		2	1	0.25
            1 members		{'y', 'x'}		1	1	0.5
            5 members		{'y', 'z'}		0	0	0
            3 members		{'w', 'z'}		1	0	0
        Calculating remaining good weights:
                Weight
            w	0.5
            x	1.0
    Family 1 chooses x
    
    Family 2 chooses a good from {'w'}:
        Calculating member weights:
                            Desired set		r	s	Weight
            2 members		{'w', 'z'}		1	1	0.5
            3 members		{'y', 'z'}		0	0	0
        Calculating remaining good weights:
                Weight
            w	1.0
    Family 2 chooses w
    Final allocation: family 1 gets {'x', 'z'}, family 2 gets {'y', 'w'}
    
    """