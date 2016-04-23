from pyhdl.primitives import *
from pyhdl.wire import Wire
import unittest


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
