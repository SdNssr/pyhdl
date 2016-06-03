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

        :param gates: An arbitrarily nested list of gates.
        :type gates: list
    """

    def __init__(self, gates):
        self.gates = flatten_list(gates)

    def eval(self):
        """
            Evaluate all the gates.
        """
        [gate.eval() for gate in self.gates]
    
    def tick(self):
        """
            Send a tick to all the gates.
        """
        [gate.tick() for gate in self.gates]
    
    def tock(self):
        """
            Send a tock to all the gates.
        """
        [gate.tock() for gate in self.gates]
