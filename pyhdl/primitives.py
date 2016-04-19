"""
    Primitive gates.
"""
from pyhdl.gate import Gate
from pyhdl.wire import Wire


class _Combinatorial(Gate):

    def tick(self):
        pass

    def tock(self):
        pass


class _TwoInputCombinatorial(_Combinatorial):

    def __init__(self, a, b, out):
        self.a = a
        self.b = b
        self.out = out
        self.register(a, b)
        self.register_output(out)
        self.eval()

    def eval(self):
        if self.a.val == "x" or self.b.val == "x":
            self.out.val = 'x'
        else:
            self.evaluate()

    def view(self, signal):
        if signal == "a":
            return self.a
        elif signal == "b":
            return self.b
        elif signal == "out":
            return self.out
        else:
            return None


class NandGate(_TwoInputCombinatorial):
    """
        A Nand Gate.
    """

    def evaluate(self):
        if (self.a.val == "1") and (self.b.val == "1"):
            self.out.val = "0"
        else:
            self.out.val = "1"


class AndGate(_TwoInputCombinatorial):
    """
        An And gate.
    """

    def evaluate(self):
        if (self.a.val == "1") and (self.b.val == "1"):
            self.out.val = "1"
        else:
            self.out.val = "0"


class NorGate(_TwoInputCombinatorial):
    """
        A Nor gate.
    """

    def evaluate(self):
        if (self.a.val == "1") or (self.b.val == "1"):
            self.out.val = "0"
        else:
            self.out.val = "1"


class OrGate(_TwoInputCombinatorial):
    """
        An Or gate.
    """

    def evaluate(self):
        if (self.a.val == "1") or (self.b.val == "1"):
            self.out.val = "1"
        else:
            self.out.val = "0"


class XorGate(_TwoInputCombinatorial):
    """
        An Xor gate.
    """

    def evaluate(self):
        if (self.a.val == "1") ^ (self.b.val == "1"):
            self.out.val = "1"
        else:
            self.out.val = "0"


class NotGate(Gate):
    """
        A Not Gate
    """

    def __init__(self, a, out):
        self.a = a
        self.out = out
        self.register(a)
        self.register_output(out)


    def tick(self):
        pass

    def tock(self):
        pass

    def eval(self):
        if self.a.val == "1":
            self.out.val = "0"
        else:
            self.out.val = "1"

    def view(self, signal):
        if signal == "a":
            return self.a
        elif signal == "out":
            return self.out
        else:
            return None


class DFF(Gate):
    """
        A D flip flop
    """

    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.register(self.input)
        self.register_output(self.output)
        self.state = None

    def tick(self):
        self.state = self.input.val

    def tock(self):
        self.output.val = self.state

    def eval(self):
        pass

    def view(self, signal):
        if signal == "input":
            return self.input
        elif signal == "output":
            return self.output
        else:
            return None
