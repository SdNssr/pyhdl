from pyhdl.composite import Composite
from pyhdl.wire import Wire
import unittest


class CompositeTest(unittest.TestCase):

    def setUp(self):
        self.inputs = {
            "a": Wire(),
            "b": Wire(),
            "c": Wire(),
        }

        self.outputs = {
            "x": Wire(),
            "y": Wire(),
            "z": Wire(),
        }

        self.internals = {
            "i1": Wire(),
            "i2": Wire(),
            "i3": Wire(),
        }

        self.gateList = [self, self, self, self]

        self.gateDict = {
            "g1": self,
            "g2": self,
            "g3": self,
        }

        self.composite = Composite(
            self.gateList,
            self.inputs,
            self.outputs,
            self.internals,
            self.gateDict
        )

        self.tick_count = 0
        self.tock_count = 0
        self.eval_count = 0

    def tick(self):
        self.tick_count += 1

    def tock(self):
        self.tock_count += 1

    def eval(self):
        self.eval_count += 1

    def test_view(self):
        assert self.composite.view('a') == self.inputs['a']
        assert self.composite.view('b') == self.inputs['b']
        assert self.composite.view('c') == self.inputs['c']
        assert self.composite.view('x') == self.outputs['x']
        assert self.composite.view('y') == self.outputs['y']
        assert self.composite.view('z') == self.outputs['z']
        assert self.composite.view('i1') == self.internals['i1']
        assert self.composite.view('i2') == self.internals['i2']
        assert self.composite.view('i3') == self.internals['i3']
        assert self.composite.view('g1') == self.gateDict['g1']
        assert self.composite.view('g2') == self.gateDict['g2']
        assert self.composite.view('g3') == self.gateDict['g3']
        assert self.composite.view('g4') is None

    def test_tick(self):
        self.composite.tick()
        assert self.tick_count == 4

    def test_tock(self):
        self.composite.tock()
        assert self.tock_count == 4

    def test_eval(self):
        self.composite.eval()
        assert self.eval_count == 4

    def test_getattr(self):
        assert self.composite.a == self.inputs['a']
        assert self.composite.b == self.inputs['b']
        assert self.composite.c == self.inputs['c']
        assert self.composite.x == self.outputs['x']
        assert self.composite.y == self.outputs['y']
        assert self.composite.z == self.outputs['z']
        assert self.composite.i1 == self.internals['i1']
        assert self.composite.i2 == self.internals['i2']
        assert self.composite.i3 == self.internals['i3']
        assert self.composite.g1 == self.gateDict['g1']
        assert self.composite.g2 == self.gateDict['g2']
        assert self.composite.g3 == self.gateDict['g3']
        with self.assertRaises(AttributeError):
            self.composite.g4
