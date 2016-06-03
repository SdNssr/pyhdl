"""
    Primitive gates.
"""
from pyhdl.gate import Gate
from pyhdl.wire import Wire
from six.moves import reduce


class _Combinatorial(Gate):

    def tick(self):
        self.eval()

    def tock(self):
        self.eval()


class _SimpleCombinatorial(_Combinatorial):

    attributes = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, width=1, ways=2, **kwargs):
        self.signals = set([self.attributes[way] for way in range(0, ways)])

        for signal in self.signals:
            wire = kwargs[signal]
            setattr(self, signal, wire)

        self.out = kwargs['out']

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
        A Xor gate.
    """

    def evaluate(self, a, b):
        if (a == "1") ^ (b == "1"):
            return "1"
        else:
            return "0"


class NotGate(_Combinatorial):
    """
        A Not Gate.

        :param inp: The input wire.
        :param out: The output wire.
        :param width: The width of the inputs.
        :type width: int
    """

    def __init__(self, inp, out, width=1):
        self.inp = inp
        self.out = out

    def tick(self):
        pass

    def tock(self):
        pass

    def eval(self):
        computed = [self.evaluate(val) for val in self.inp.val]
        self.out.val = ''.join(computed)

    def evaluate(self, inp):
        if inp == 'x':
            return 'x'
        elif inp == "1":
            return "0"
        else:
            return "1"

    def view(self, signal):
        if signal == "inp":
            return self.inp
        elif signal == "out":
            return self.out
        else:
            return None


class Multiplexer(_Combinatorial):
    """
        A Multiplexer.

        Named parameters from 'a' to 'z' are used as inputs. e.g.::

            from pyhdl import *
            a, b, c, d = Wire(), Wire(), Wire(), Wire()
            sel = Wire(width=2)
            out = Wire()
            nand = Multiplexer(a=a, b=b, c=c, d=d, out=out, sel=sel, ways=4)

        :param out: The output wire.
        :param sel: The selector wire.
        :param width: The width of the inputs.
        :type width: int
        :param ways: The number of inputs to the multiplexer.
        :type ways: int
    """

    attributes = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, width=1, ways=2, **kwargs):
        self.signals = [self.attributes[way] for way in range(0, ways)]

        for signal in self.signals:
            wire = kwargs[signal]
            setattr(self, signal, wire)

        self.out = kwargs['out']
        self.sel = kwargs['sel']

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
        A Demultiplexer.

        Named parameters from 'a' to 'z' are used as outputs. e.g.::

            from pyhdl import *
            a, b, c, d = Wire(), Wire(), Wire(), Wire()
            sel = Wire(width=2)
            input = Wire()
            nand = Multiplexer(a=a, b=b, c=c, d=d, input=input, sel=sel, ways=4)

        :param input: The input wire.
        :param sel: The selector wire.
        :param width: The width of the outputs.
        :type width: int
        :param ways: The number of outputs from the demultiplexer.
        :type ways: int

    """

    attributes = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, width=1, ways=2, **kwargs):
        self.width = width
        self.ways = ways

        self.signals = [self.attributes[way] for way in range(0, ways)]

        for signal in self.signals:
            wire = kwargs[signal]
            setattr(self, signal, wire)

        self.input = kwargs['input']
        self.sel = kwargs['sel']


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

        :param a: The first operand of the half adder.
        :param b: The second operand of the half adder.
        :param out: The output of the half adder.
        :param carry: The carry output from the half adder.
    """

    def __init__(self, a, b, out, carry):
        self.a = a
        self.b = b

        self.out = out
        self.carry = carry



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


class FullAdder(_Combinatorial):
    """
        A full adder.

        :param a: The first operand of the half adder.
        :param b: The second operand of the half adder.
        :param cin: The carry input to the half adder.
        :param out: The output of the half adder.
        :param cout: The carry output from the half adder.
    """

    values = {
        ('0', '0', '0'): ('0', '0'),
        ('0', '0', '1'): ('1', '0'),
        ('0', '1', '0'): ('1', '0'),
        ('0', '1', '1'): ('0', '1'),
        ('1', '0', '0'): ('1', '0'),
        ('1', '0', '1'): ('0', '1'),
        ('1', '1', '0'): ('0', '1'),
        ('1', '1', '1'): ('1', '1'),
    }

    def __init__(self, a, b, cin, out, cout):
        self.a = a
        self.b = b
        self.cin = cin

        self.out = out
        self.cout = cout



    def eval(self):
        if (self.a.val == 'x') or (self.b.val == 'x') or (self.cin.val == 'x'):
            self.out.val = 'x'
            self.cout.val = 'x'
            return

        self.out.val, self.cout.val = self.values[(self.a.val, self.b.val, self.cin.val)]

    def view(self, signal):
        if signal == "a":
            return self.a
        elif signal == "b":
            return self.b
        elif signal == "cin":
            return self.cin
        elif signal == "out":
            return self.out
        elif signal == "cout":
            return self.cout
        else:
            return None


class Adder(_Combinatorial):
    """
        An adder.

        :param a: The first operand of the adder.
        :param b: The second operand of the adder.
        :param out: The output of the adder.
        :param cout: The carry out flag from the adder.
        :param width: The width of the adder.
    """


    def __init__(self, a, b, out, cout, width=1):
        self.width = width
        self.size = (1 << width) - 1
        self.a = a
        self.b = b

        self.out = out
        self.cout = cout


    def eval(self):
        if ('x' in self.a.val) or ('x' in self.b.val):
            self.out.val = 'x' * self.width
            self.cout.val = 'x' * self.width
            return

        s = self.a.uival + self.b.uival

        self.out.uival = s

        if self.out.uival != s:
            self.cout.val = '1'
        else:
            self.cout.val = '0'

    def view(self, signal):
        if signal == "a":
            return self.a
        elif signal == "b":
            return self.b
        elif signal == "out":
            return self.out
        elif signal == "cout":
            return self.cout
        else:
            return None


class DFF(Gate):
    """
        A D flip flop.

        :param input: The input to the DFF.
        :param output: The output from the DFF.
        :param default: The default value of the DFF.
    """

    def __init__(self, input, output, default):
        self.input = input
        self.output = output
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


class Register(Gate):
    """
        A variable width register.

        :param input: The input value to the register.
        :param write: The write enable wire.
        :param output: The output value from the register.
        :param default: The default value of the register.
        :type default: str
    """

    def __init__(self, input, write, output, default):
        self.input = input
        self.write = write
        self.output = output
        self.state = default


        self.output.val = default

    def tick(self):
        if self.write.val == '1':
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
        elif signal == "write":
            return self.write
        else:
            return None


class Memory(Gate):
    """
        A variable width and depth memory.

        :param input:   The input value to the memory.
        :param output:  The output value from the memory.
        :param write:   The write enable wire.
        :param address: The address wire.
        :param default: The default contents of the memory.
        :type default: dict
        :param width:   The width of the memory.
        :type width: int
    """

    def __init__(self, input, output, write, address, default, width=1):
        self.input = input
        self.output = output
        self.write = write
        self.address = address
        self.width = width

        self.default = default
        self.memory = {}

    def eval(self):
        pass

    def tick(self):
        if 'x' in self.address.val:
            self.output.val = self.width * 'x'
            return

        if self.write.val == '1':
            addr = self.address.uival
            self.memory[addr] = self.input.uival

    def tock(self):
        if 'x' in self.address.val:
            self.output.val = self.width * 'x'
            return

        addr = self.address.uival
        if addr in self.memory:
            self.output.uival = self.memory[addr]
        else:
            self.output.uival = self.default

    def view(self, signal):
        if signal == "input":
            return self.input
        elif signal == "output":
            return self.output
        elif signal == "write":
            return self.write
        elif signal == "address":
            return self.address
        else:
            return None
