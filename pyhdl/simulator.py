"""
    A simulator for composite gates.

    You can supply an arbitrarily nested list of gates, sorted in topological order.
"""


def flatten_list(l):
    """
        Flatten an arbitrarily nested list.
    """
    out = []
    for x in l:
        if isinstance(x, (list, tuple)):
            out.extend(flatten_list(x))
        else:
            out.append(x)
    return out


class Simulator(object):
    """
        A simulator for composite gates.
    """

    def __init__(self, gates):
        self.gates = flatten_list(gates)

    def eval(self):
        [gate.eval() for gate in self.gates]
    
    def tick(self):
        [gate.tick() for gate in self.gates]
    
    def tock(self):
        [gate.tock() for gate in self.gates]
