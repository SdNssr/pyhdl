from nose.tools import set_trace
from pyhdl.primitives import *
from pyhdl.wire import Wire
import unittest
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


class TestNandGate(TwoInputTest, unittest.TestCase):

    gate = NandGate

    def test_tt(self):
        self.a.val, self.b.val = "1", "1"
        self.assertEqual(self.out.val, "0")

    def test_tf(self):
        self.a.val, self.b.val = "1", "0"
        self.assertEqual(self.out.val, "1")

    def test_ft(self):
        self.a.val, self.b.val = "0", "1"
        self.assertEqual(self.out.val, "1")

    def test_ff(self):
        self.a.val, self.b.val = "0", "0"
        self.assertEqual(self.out.val, "1")

    def test_default(self):
        self.assertEqual(self.out.val, "x")


class TestAndGate(TwoInputTest, unittest.TestCase):

    gate = AndGate

    def test_tt(self):
        self.a.val, self.b.val = "1", "1"
        self.assertEqual(self.out.val, "1")

    def test_tf(self):
        self.a.val, self.b.val = "1", "0"
        self.assertEqual(self.out.val, "0")

    def test_ft(self):
        self.a.val, self.b.val = "0", "1"
        self.assertEqual(self.out.val, "0")

    def test_ff(self):
        self.a.val, self.b.val = "0", "0"
        self.assertEqual(self.out.val, "0")

    def test_default(self):
        self.assertEqual(self.out.val, "x")


class TestNorGate(TwoInputTest, unittest.TestCase):

    gate = NorGate

    def test_tt(self):
        self.a.val, self.b.val = "1", "1"
        self.assertEqual(self.out.val, "0")

    def test_tf(self):
        self.a.val, self.b.val = "1", "0"
        self.assertEqual(self.out.val, "0")

    def test_ft(self):
        self.a.val, self.b.val = "0", "1"
        self.assertEqual(self.out.val, "0")

    def test_ff(self):
        self.a.val, self.b.val = "0", "0"
        self.assertEqual(self.out.val, "1")

    def test_default(self):
        self.assertEqual(self.out.val, "x")


class TestOrGate(TwoInputTest, unittest.TestCase):

    gate = OrGate

    def test_tt(self):
        self.a.val, self.b.val = "1", "1"
        self.assertEqual(self.out.val, "1")

    def test_tf(self):
        self.a.val, self.b.val = "1", "0"
        self.assertEqual(self.out.val, "1")

    def test_ft(self):
        self.a.val, self.b.val = "0", "1"
        self.assertEqual(self.out.val, "1")

    def test_ff(self):
        self.a.val, self.b.val = "0", "0"
        self.assertEqual(self.out.val, "0")

    def test_default(self):
        self.assertEqual(self.out.val, "x")


class TestXorGate(TwoInputTest, unittest.TestCase):

    gate = XorGate

    def test_tt(self):
        self.a.val, self.b.val = "1", "1"
        self.assertEqual(self.out.val, "0")

    def test_tf(self):
        self.a.val, self.b.val = "1", "0"
        self.assertEqual(self.out.val, "1")

    def test_ft(self):
        self.a.val, self.b.val = "0", "1"
        self.assertEqual(self.out.val, "1")

    def test_ff(self):
        self.a.val, self.b.val = "0", "0"
        self.assertEqual(self.out.val, "0")

    def test_default(self):
        self.assertEqual(self.out.val, "x")


class TestNotGate(unittest.TestCase):

    def setUp(self):
        self.a, self.out = Wire(), Wire()
        self.not_gate = NotGate(self.a, self.out)

    def test_ticktock(self):
        self.not_gate.tick()
        self.not_gate.tock()
        self.test_default()

    def test_t(self):
        self.a.val = "1"
        self.assertEqual(self.out.val, "0")

    def test_f(self):
        self.a.val = "0"
        self.assertEqual(self.out.val, "1")

    def test_default(self):
        self.assertEqual(self.out.val, "x")

    def test_view(self):
        assert self.not_gate.view('a') == self.a
        assert self.not_gate.view('out') == self.out
        assert self.not_gate.view('garbage') is None


class TestMultiplexer(unittest.TestCase):

    def setUp(self):
        self.a = Wire(width=3)
        self.b = Wire(width=3)
        self.c = Wire(width=3)
        self.d = Wire(width=3)

        self.a.val = '010'
        self.b.val = '111'
        self.c.val = '110'
        self.d.val = '011'

        self.sel = Wire(width=2)
        self.out = Wire(width=3)

        self.mux = Multiplexer(
            a=self.a, 
            b=self.b, 
            c=self.c, 
            d=self.d, 
            sel=self.sel, 
            out=self.out,
            width=3,
            ways=4
        )

    def test_default(self):
        self.assertEqual(self.out.val, 'xxx')

    def test_sel(self):
        self.sel.val = '00'
        self.assertEqual(self.out.val, '010')
        self.sel.val = '01'
        self.assertEqual(self.out.val, '111')
        self.sel.val = '10'
        self.assertEqual(self.out.val, '110')
        self.sel.val = '11'
        self.assertEqual(self.out.val, '011')


    def test_view(self):
        self.assertEqual(self.mux.view('a'), self.a)
        self.assertEqual(self.mux.view('b'), self.b)
        self.assertEqual(self.mux.view('c'), self.c)
        self.assertEqual(self.mux.view('d'), self.d)
        self.assertEqual(self.mux.view('out'), self.out)
        self.assertEqual(self.mux.view('sel'), self.sel)
        self.assertEqual(self.mux.view('garbage'), None)


class TestDemultiplexer(unittest.TestCase):

    def setUp(self):
        self.a = Wire(width=3)
        self.b = Wire(width=3)
        self.c = Wire(width=3)
        self.d = Wire(width=3)

        self.sel = Wire(width=2)
        self.input = Wire(width=3)

        self.input.val = '101'

        self.demux = Demultiplexer(
            a=self.a, 
            b=self.b, 
            c=self.c, 
            d=self.d, 
            sel=self.sel, 
            input=self.input,
            width=3,
            ways=4
        )

    def test_default(self):
        self.assertEqual(self.a.val, 'xxx')
        self.assertEqual(self.b.val, 'xxx')
        self.assertEqual(self.c.val, 'xxx')
        self.assertEqual(self.d.val, 'xxx')

    def test_sel(self):
        self.sel.val = '00'
        self.assertEqual(self.a.val, '101')
        self.assertEqual(self.b.val, '000')
        self.assertEqual(self.c.val, '000')
        self.assertEqual(self.d.val, '000')
        self.sel.val = '01'
        self.assertEqual(self.a.val, '000')
        self.assertEqual(self.b.val, '101')
        self.assertEqual(self.c.val, '000')
        self.assertEqual(self.d.val, '000')
        self.sel.val = '10'
        self.assertEqual(self.a.val, '000')
        self.assertEqual(self.b.val, '000')
        self.assertEqual(self.c.val, '101')
        self.assertEqual(self.d.val, '000')
        self.sel.val = '11'
        self.assertEqual(self.a.val, '000')
        self.assertEqual(self.b.val, '000')
        self.assertEqual(self.c.val, '000')
        self.assertEqual(self.d.val, '101')


    def test_view(self):
        self.assertEqual(self.demux.view('a'), self.a)
        self.assertEqual(self.demux.view('b'), self.b)
        self.assertEqual(self.demux.view('c'), self.c)
        self.assertEqual(self.demux.view('d'), self.d)
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
        self.assertEqual(self.out.val, "0")
        self.assertEqual(self.carry.val, "1")

    def test_tf(self):
        self.a.val, self.b.val = "1", "0"
        self.assertEqual(self.out.val, "1")
        self.assertEqual(self.carry.val, "0")

    def test_ft(self):
        self.a.val, self.b.val = "0", "1"
        self.assertEqual(self.out.val, "1")
        self.assertEqual(self.carry.val, "0")

    def test_ff(self):
        self.a.val, self.b.val = "0", "0"
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
        self.cout = Wire(width=16)

        self.adder = Adder(a=self.a, b=self.b, out=self.out, cout=self.cout, width=16)

    def test_view(self):
        self.assertEqual(self.adder.view('a'), self.a)
        self.assertEqual(self.adder.view('b'), self.b)
        self.assertEqual(self.adder.view('out'), self.out)
        self.assertEqual(self.adder.view('cout'), self.cout)
        self.assertEqual(self.adder.view('garbage'), None)

    def test_ticktock(self):
        self.adder.tick()
        self.adder.tock()
        self.test_default()

    def test_default(self):
        self.assertEqual(self.out.val, 'xxxxxxxxxxxxxxxx')
        self.assertEqual(self.cout.val, 'xxxxxxxxxxxxxxxx')

    def assertVals(self, a, b):
        self.a.ival = a
        self.b.ival = b
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
