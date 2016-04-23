"""
    Primitive gates.
"""
from pyhdl.gate import Gate
from pyhdl.wire import Wire
from six.moves import reduce


class _Combinatorial(Gate):

    def tick(self):
        pass

    def tock(self):
        pass


class _SimpleCombinatorial(_Combinatorial):

    attributes = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, width=1, ways=2, **kwargs):
        self.signals = set([self.attributes[way] for way in range(0, ways)])

        for signal in self.signals:
            wire = kwargs[signal]

            setattr(self, signal, wire)

            self.register(wire)

        self.out = kwargs['out']
        self.register_output(self.out)

    def eval(self):
        vals = [getattr(self, signal).val for signal in self.signals]
        computed = [reduce(self.biteval, seq) for seq in zip(*vals)]
        self.out.val = ''.join(computed)

    def biteval(self, a, b):
        if (a == "x") or (b == "x"):
            return 'x'
        else:
            return self.evaluate(a, b)

    def view(self, signal):
        if signal in self.signals:
            return getattr(self, signal)
        elif signal == 'out':
            return self.out
        else:
            return None

class NandGate(_SimpleCombinatorial):
    """
        A Nand Gate.
    """

    def evaluate(self, a, b):
        if (a == "1") and (b == "1"):
            return "0"
        else:
            return "1"


class AndGate(_SimpleCombinatorial):
    """
        An And gate.
    """

    def evaluate(self, a, b):
        if (a == "1") and (b == "1"):
            return "1"
        else:
            return "0"


class NorGate(_SimpleCombinatorial):
    """
        A Nor gate.
    """

    def evaluate(self, a, b):
        if (a == "1") or (b == "1"):
            return "0"
        else:
            return "1"


class OrGate(_SimpleCombinatorial):
    """
        An Or gate.
    """

    def evaluate(self, a, b):
        if (a == "1") or (b == "1"):
            return "1"
        else:
            return "0"


class XorGate(_SimpleCombinatorial):
    """
        An Xor gate.
    """

    def evaluate(self, a, b):
        if (a == "1") ^ (b == "1"):
            return "1"
        else:
            return "0"


class NotGate(_Combinatorial):
    """
        A Not Gate
    """

    def __init__(self, a, out, width=1):
        self.a = a
        self.out = out
        self.register(a)
        self.register_output(out)

    def tick(self):
        pass

    def tock(self):
        pass

    def eval(self):
        computed = [self.evaluate(val) for val in self.a.val]
        self.out.val = ''.join(computed)

    def evaluate(self, a):
        if a == 'x':
            return 'x'
        elif a == "1":
            return "0"
        else:
            return "1"

    def view(self, signal):
        if signal == "a":
            return self.a
        elif signal == "out":
            return self.out
        else:
            return None


class Multiplexer(_Combinatorial):
    """
        A Multiplexer
    """

    attributes = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, width=1, ways=2, **kwargs):
        self.signals = [self.attributes[way] for way in range(0, ways)]

        for signal in self.signals:
            wire = kwargs[signal]

            setattr(self, signal, wire)

            self.register(wire)

        self.out = kwargs['out']
        self.register_output(self.out)

        self.sel = kwargs['sel']
        self.register(self.sel)

    def eval(self):
        if 'x' in self.sel.val:
            return
        else:
            vals = [getattr(self, signal).val for signal in self.signals]
            selection = int(self.sel.val, 2)
            self.out.val = vals[selection]

    def view(self, signal):
        if signal in self.signals:
            return getattr(self, signal)
        elif signal == 'out':
            return self.out
        elif signal == 'sel':
            return self.sel
        else:
            return None


class Demultiplexer(_Combinatorial):
    """
        A Demultiplexer
    """

    attributes = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, width=1, ways=2, **kwargs):
        self.width = width
        self.ways = ways

        self.signals = [self.attributes[way] for way in range(0, ways)]

        for signal in self.signals:
            wire = kwargs[signal]

            setattr(self, signal, wire)

            self.register_output(wire)

        self.input = kwargs['input']
        self.sel = kwargs['sel']

        self.register(self.sel)
        self.register(self.input)

    def eval(self):
        if 'x' in self.sel.val:
            return
        else:
            selection = int(self.sel.val, 2)

            for x in range(0, self.ways):
                name = self.signals[x]

                if x == selection:
                    getattr(self, name).val = self.input.val
                else:
                    getattr(self, name).val = '0' * self.width

    def view(self, signal):
        if signal in self.signals:
            return getattr(self, signal)
        elif signal == 'input':
            return self.input
        elif signal == 'sel':
            return self.sel
        else:
            return None


class HalfAdder(_Combinatorial):
    """
        A half adder.
    """

    def __init__(self, a, b, out, carry):
        self.a = a
        self.b = b

        self.out = out
        self.carry = carry

        self.register(self.a, self.b)

        self.register_output(self.out)
        self.register_output(self.carry)

    def eval(self):
        if (self.a.val == 'x') or (self.b.val == 'x'):
            self.out.val = 'x'
            self.carry.val = 'x'
            return

        if (self.a.val == '1') ^ (self.b.val == '1'):
            self.out.val = '1'
        else:
            self.out.val = '0'

        if (self.a.val == '1') and (self.b.val == '1'):
            self.carry.val = '1'
        else:
            self.carry.val = '0'

    def view(self, signal):
        if signal == "a":
            return self.a
        elif signal == "b":
            return self.b
        elif signal == "out":
            return self.out
        elif signal == "carry":
            return self.carry
        else:
            return None


class DFF(Gate):
    """
        A D flip flop
    """

    def __init__(self, input, output, default):
        self.input = input
        self.output = output
        self.register(self.input)
        self.register_output(self.output)
        self.state = default
        self.output.val = default

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
