#!python3

"""
Short utils used for demonstration and presentation
"""



def plural(i: int)->str:
    return " " if i==1 else "s"



def demo(algorithm, families, goods, *args):
    """
    Demonstrate the given algorithm on the given families (must be 2 families).
    """
    if len(families)!=2:
        raise("Currently only 2 families are supported")
    for family in families:
        print(family)
    bundles = algorithm(families, goods, *args)
    print("\nFinal allocation:\n * {}\n * {}".format(
        families[0].allocation_description(bundles[0], bundles),
        families[1].allocation_description(bundles[1], bundles)))

