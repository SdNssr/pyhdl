from nose.tools import set_trace
from pyhdl.primitives import *
from pyhdl.wire import Wire
import unittest
import random
import ctypes


class TwoInputTest(object):

    def setUp(self):
        self.a, self.b, self.out = Wire(), Wire(), Wire()
        self.and_gate = self.gate(a=self.a, b=self.b, out=self.out)

    def test_view(self):
        assert self.and_gate.view('a') == self.a
        assert self.and_gate.view('b') == self.b
        assert self.and_gate.view('out') == self.out
        assert self.and_gate.view('garbage') is None

    def test_ticktock(self):
        self.and_gate.tick()
        self.and_gate.tock()
        self.test_default()

    def assertVal(self, a, b, out):
        self.a.val = a
        self.b.val = b
        self.and_gate.eval()

        self.assertEqual(self.out.val, out)


class TestNandGate(TwoInputTest, unittest.TestCase):

    gate = NandGate

    def test_values(self):
        self.assertVal('1', '1', '0')
        self.assertVal('1', '0', '1')
        self.assertVal('0', '1', '1')
        self.assertVal('0', '0', '1')

    def test_default(self):
        self.assertEqual(self.out.val, "x")


class TestAndGate(TwoInputTest, unittest.TestCase):

    gate = AndGate

    def test_values(self):
        self.assertVal('1', '1', '1')
        self.assertVal('1', '0', '0')
        self.assertVal('0', '1', '0')
        self.assertVal('0', '0', '0')

    def test_default(self):
        self.assertEqual(self.out.val, "x")


class TestNorGate(TwoInputTest, unittest.TestCase):

    gate = NorGate

    def test_values(self):
        self.assertVal('1', '1', '0')
        self.assertVal('1', '0', '0')
        self.assertVal('0', '1', '0')
        self.assertVal('0', '0', '1')

    def test_default(self):
        self.assertEqual(self.out.val, "x")


class TestOrGate(TwoInputTest, unittest.TestCase):

    gate = OrGate

    def test_values(self):
        self.assertVal('1', '1', '1')
        self.assertVal('1', '0', '1')
        self.assertVal('0', '1', '1')
        self.assertVal('0', '0', '0')

    def test_default(self):
        self.assertEqual(self.out.val, "x")


class TestXorGate(TwoInputTest, unittest.TestCase):

    gate = XorGate

    def test_values(self):
        self.assertVal('1', '1', '0')
        self.assertVal('1', '0', '1')
        self.assertVal('0', '1', '1')
        self.assertVal('0', '0', '0')

    def test_default(self):
        self.assertEqual(self.out.val, "x")


class TestNotGate(unittest.TestCase):

    def setUp(self):
        self.inp, self.out = Wire(), Wire()
        self.not_gate = NotGate(self.inp, self.out)

    def test_ticktock(self):
        self.not_gate.tick()
        self.not_gate.tock()
        self.test_default()

    def assertVal(self, inp, out):
        self.inp.val = inp
        self.not_gate.eval()
        self.assertEqual(self.out.val, out)

    def test_vals(self):
        self.assertVal('0', '1')
        self.assertVal('1', '0')

    def test_default(self):
        self.assertEqual(self.out.val, "x")

    def test_view(self):
        assert self.not_gate.view('inp') == self.inp
        assert self.not_gate.view('out') == self.out
        assert self.not_gate.view('garbage') is None


class TestMultiplexer(unittest.TestCase):

    def setUp(self):
        self.inputs = [
            Wire(width=3),
            Wire(width=3),
            Wire(width=3),
            Wire(width=3),
        ]

        self.sel = Wire(width=2)
        self.out = Wire(width=3)

        self.mux = Multiplexer(
            a=self.inputs[0], 
            b=self.inputs[1], 
            c=self.inputs[2], 
            d=self.inputs[3], 
            sel=self.sel, 
            out=self.out,
            width=3,
            ways=4
        )

    def fuzzyEval(self):
        for input in self.inputs:
            input.uival = random.randrange(0, 8)
        self.sel.uival = random.randrange(0, 4)
        self.mux.eval()
        self.assertEqual(self.inputs[self.sel.uival].val, self.out.val)

    def test_default(self):
        self.assertEqual(self.out.val, 'xxx')

    def test_sel(self):
        for x in range(0, 10):
            self.fuzzyEval()

    def test_view(self):
        self.assertEqual(self.mux.view('a'), self.inputs[0])
        self.assertEqual(self.mux.view('b'), self.inputs[1])
        self.assertEqual(self.mux.view('c'), self.inputs[2])
        self.assertEqual(self.mux.view('d'), self.inputs[3])
        self.assertEqual(self.mux.view('out'), self.out)
        self.assertEqual(self.mux.view('sel'), self.sel)
        self.assertEqual(self.mux.view('garbage'), None)


class TestDemultiplexer(unittest.TestCase):

    def setUp(self):
        self.outputs = [
            Wire(width=3),
            Wire(width=3),
            Wire(width=3),
            Wire(width=3),
        ]

        self.sel = Wire(width=2)
        self.input = Wire(width=3)

        self.demux = Demultiplexer(
            a=self.outputs[0], 
            b=self.outputs[1], 
            c=self.outputs[2], 
            d=self.outputs[3], 
            sel=self.sel, 
            input=self.input,
            width=3,
            ways=4
        )

    def fuzzyEval(self):
        self.input.uival = random.randrange(0, 8)
        self.sel.uival = random.randrange(0, 4)
        self.demux.eval()
        self.assertEqual(self.outputs[self.sel.uival].val, self.input.val)

    def test_default(self):
        for output in self.outputs:
            self.assertEqual(output.val, 'xxx')

    def test_sel(self):
        for x in range(0, 10):
            self.fuzzyEval()

    def test_view(self):
        self.assertEqual(self.demux.view('a'), self.outputs[0])
        self.assertEqual(self.demux.view('b'), self.outputs[1])
        self.assertEqual(self.demux.view('c'), self.outputs[2])
        self.assertEqual(self.demux.view('d'), self.outputs[3])
        self.assertEqual(self.demux.view('input'), self.input)
        self.assertEqual(self.demux.view('sel'), self.sel)
        self.assertEqual(self.demux.view('garbage'), None)


class TestHalfAdder(unittest.TestCase):

    def setUp(self):
        self.a = Wire()
        self.b = Wire()
        self.out = Wire()
        self.carry = Wire()

        self.adder = HalfAdder(a=self.a, b=self.b, out=self.out, carry=self.carry)

    def test_view(self):
        self.assertEqual(self.adder.view('a'), self.a)
        self.assertEqual(self.adder.view('b'), self.b)
        self.assertEqual(self.adder.view('out'), self.out)
        self.assertEqual(self.adder.view('carry'), self.carry)
        self.assertEqual(self.adder.view('garbage'), None)

    def test_ticktock(self):
        self.adder.tick()
        self.adder.tock()
        self.test_default()

    def test_default(self):
        self.assertEqual(self.out.val, 'x')
        self.assertEqual(self.carry.val, 'x')

    def test_tt(self):
        self.a.val, self.b.val = "1", "1"
        self.adder.eval()
        self.assertEqual(self.out.val, "0")
        self.assertEqual(self.carry.val, "1")

    def test_tf(self):
        self.a.val, self.b.val = "1", "0"
        self.adder.eval()
        self.assertEqual(self.out.val, "1")
        self.assertEqual(self.carry.val, "0")

    def test_ft(self):
        self.a.val, self.b.val = "0", "1"
        self.adder.eval()
        self.assertEqual(self.out.val, "1")
        self.assertEqual(self.carry.val, "0")

    def test_ff(self):
        self.a.val, self.b.val = "0", "0"
        self.adder.eval()
        self.assertEqual(self.out.val, "0")
        self.assertEqual(self.carry.val, "0")


class TestFullAdder(unittest.TestCase):

    def setUp(self):
        self.a = Wire()
        self.b = Wire()
        self.cin = Wire()
        self.out = Wire()
        self.cout = Wire()

        self.adder = FullAdder(a=self.a, b=self.b, out=self.out, cin=self.cin, cout=self.cout)

    def test_view(self):
        self.assertEqual(self.adder.view('a'), self.a)
        self.assertEqual(self.adder.view('b'), self.b)
        self.assertEqual(self.adder.view('out'), self.out)
        self.assertEqual(self.adder.view('cout'), self.cout)
        self.assertEqual(self.adder.view('cin'), self.cin)
        self.assertEqual(self.adder.view('garbage'), None)

    def test_ticktock(self):
        self.adder.tick()
        self.adder.tock()
        self.test_default()

    def test_default(self):
        self.assertEqual(self.out.val, 'x')
        self.assertEqual(self.cout.val, 'x')

    def assertVals(self, a, b, cin, out, cout):
        self.a.val = a
        self.b.val = b
        self.cin.val = cin
        self.adder.eval()
        self.assertEqual(self.out.val, out)
        self.assertEqual(self.cout.val, cout)

    def test_functionality(self):
        self.assertVals('0', '0', '0', '0', '0')
        self.assertVals('0', '0', '1', '1', '0')
        self.assertVals('0', '1', '0', '1', '0')
        self.assertVals('0', '1', '1', '0', '1')
        self.assertVals('1', '0', '0', '1', '0')
        self.assertVals('1', '0', '1', '0', '1')
        self.assertVals('1', '1', '0', '0', '1')
        self.assertVals('1', '1', '1', '1', '1')


class TestAdder(unittest.TestCase):

    def setUp(self):
        self.a = Wire(width=16)
        self.b = Wire(width=16)
        self.out = Wire(width=16)

        self.adder = Adder(a=self.a, b=self.b, out=self.out, width=16)

    def test_view(self):
        self.assertEqual(self.adder.view('a'), self.a)
        self.assertEqual(self.adder.view('b'), self.b)
        self.assertEqual(self.adder.view('out'), self.out)
        self.assertEqual(self.adder.view('garbage'), None)

    def test_ticktock(self):
        self.adder.tick()
        self.adder.tock()
        self.test_default()

    def test_default(self):
        self.assertEqual(self.out.val, 'xxxxxxxxxxxxxxxx')

    def assertVals(self, a, b):
        self.a.ival = a
        self.b.ival = b
        self.adder.eval()
        out = ctypes.c_int16(a + b).value
        self.assertEqual(self.out.ival, out)

    def test_functionality(self):
        self.assertVals(20, 30)
        self.assertVals(40, 70)
        self.assertVals(892, 243)
        self.assertVals(893, -809)
        self.assertVals(16384, 16384)
        self.assertVals(8098, -14359)


class TestDFFGate(unittest.TestCase):

    def setUp(self):
        self.a, self.out = Wire(), Wire()
        self.dff_gate = DFF(self.a, self.out, '0')

    def test_default(self):
        self.assertEqual(self.out.val, '0')

    def test_set(self):
        self.a.val = "1"
        self.dff_gate.tick()
        self.dff_gate.tock()
        self.assertEqual(self.out.val, "1")

    def test_hold(self):
        self.a.val = "1"
        self.dff_gate.tick()
        self.a.val = "0"
        self.dff_gate.tock()
        self.assertEqual(self.out.val, "1")

    def test_view(self):
        assert self.dff_gate.view('input') == self.a
        assert self.dff_gate.view('output') == self.out
        assert self.dff_gate.view('garbage') is None


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.input = Wire(width=4)
        self.output = Wire(width=4)
        self.write = Wire()
        self.register = Register(input=self.input, output=self.output, write=self.write, default='0000')

    def test_default(self):
        self.assertEqual(self.output.val, '0000')

    def test_hold(self):
        self.input.uival = 4
        self.register.tick()
        self.register.tock()
        self.test_default()

    def test_set(self):
        self.input.uival = 4
        self.write.val = '1'
        self.register.tick()
        self.input.uival = 3
        self.register.tock()
        self.assertEqual(self.output.uival, 4)

    def test_view(self):
        assert self.register.view('input') == self.input
        assert self.register.view('output') == self.output
        assert self.register.view('write') == self.write
        assert self.register.view('garbage') is None


class TestMemory(unittest.TestCase):

    def setUp(self):
        self.input = Wire(width=16)
        self.output = Wire(width=16)
        self.address = Wire(width=16)
        self.write = Wire()
        self.memory = Memory(input=self.input, output=self.output, address=self.address, write=self.write, default=0, width=16)

    def test_default(self):
        self.assertEqual(self.output.val, 'x'*16)

    def test_default_ticktock(self):
        self.memory.tick(), self.memory.tock()
        self.test_default()

    def test_default_value(self):
        self.address.uival = 1223
        self.memory.tick(), self.memory.tock()
        self.assertEqual(self.output.val, '0'*16)

    def test_store(self):
        self.address.uival = 323
        self.input.uival = 2324
        self.write.val = '1'
        self.memory.tick()
        self.write.val = '0' 
        self.memory.tock(), self.memory.tick(), self.memory.tock()
        self.assertEqual(self.output.uival, 2324)

    def test_view(self):
        self.assertEqual(self.memory.view('input'), self.input)
        self.assertEqual(self.memory.view('output'), self.output)
        self.assertEqual(self.memory.view('address'), self.address)
        self.assertEqual(self.memory.view('write'), self.write)
        self.assertEqual(self.memory.view('dfdfs'), None)
