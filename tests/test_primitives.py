from pyhdl.primitives import *
from pyhdl.wire import Wire
import unittest


class TwoInputTest(object):

    def setUp(self):
        self.a, self.b, self.out = Wire(), Wire(), Wire()
        self.and_gate = self.gate(self.a, self.b, self.out)

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
