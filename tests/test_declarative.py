from pyhdl.declarative import Module, ModuleMetaClass
from pyhdl.wire import Wire, BridgeWire
from pyhdl.primitives import NandGate
from pyhdl.utils import HDLError
import unittest


class ModuleTest(unittest.TestCase):

    def setUp(self):
        self.module = type('TestModule', Module.__bases__,
                           dict(Module.__dict__))

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

        self.gateList = []

        self.gateDict = {}

        setattr(self.module, '_pyhdl_stuff', {
            'gate_list': self.gateList,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'internals': self.internals,
            'gates': self.gateDict,
        })

        self.a = Wire()
        self.z = Wire()

        self.composite = self.module(a=self.a, z=self.z)

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
        assert self.composite.view('a') is not None
        assert self.composite.view('b') is not None
        assert self.composite.view('c') is not None
        assert self.composite.view('x') is not None
        assert self.composite.view('y') is not None
        assert self.composite.view('z') is not None
        assert self.composite.view('i1') is not None
        assert self.composite.view('i2') is not None
        assert self.composite.view('i3') is not None
        assert self.composite.view('g4') == None

    def test_tick(self):
        self.composite.tick()
        assert self.tick_count == 0

    def test_tock(self):
        self.composite.tock()
        assert self.tock_count == 0

    def test_eval(self):
        self.composite.eval()
        assert self.eval_count == 0

    def test_getattr(self):
        assert self.composite.a is not None
        assert self.composite.b is not None
        assert self.composite.c is not None
        assert self.composite.x is not None
        assert self.composite.y is not None
        assert self.composite.z is not None
        assert self.composite.i1 is not None
        assert self.composite.i2 is not None
        assert self.composite.i3 is not None
        with self.assertRaises(AttributeError):
            self.composite.g4

    def test_bridgewire(self):
        self.a.val = '1'
        assert self.composite.a.val == '1'

        self.composite.z.val = '0'
        assert self.z.val == '0'


class ModuleMetaClassTest(unittest.TestCase):

    def test_topological_sort(self):
        graph = {
            "a": ["b", "c"],
            "b": ["c"],
            "c": []
        }

        topo = ModuleMetaClass.topological_sort(graph)

        assert topo[0] == 'a'
        assert topo[1] == 'b'
        assert topo[2] == 'c'

    def test_topological_sort_cyclic(self):
        graph = {
            "a": ["b", "c"],
            "b": ["a"],
            "c": ["a"],
        }

        with self.assertRaises(HDLError):
            ModuleMetaClass.topological_sort(graph)

    def test_new(self):
        a = Wire(type="input")
        b = Wire(type="input")
        c = Wire()
        d = Wire(type="output")
        e = Wire(type="output")

        g1 = NandGate(a=a, b=b, out=c)
        g2 = NandGate(a=c, b=c, out=d)
        g3 = NandGate(a=d, b=c, out=e)

        classdict = {
            "a": a,
            "b": b,
            "c": c,
            "d": d,
            "e": e,
            "g1": g1,
            "g2": g2,
            "g3": g3,
        }

        module = ModuleMetaClass('TestModule', (Module, ), dict(classdict))

        pyhdl_stuff = getattr(module, '_pyhdl_stuff')

        assert pyhdl_stuff['gates']['g1'] == g1
        assert pyhdl_stuff['gates']['g2'] == g2
        assert pyhdl_stuff['gates']['g3'] == g3
        assert pyhdl_stuff['gate_list'][0] == g1
        assert pyhdl_stuff['gate_list'][1] == g2
        assert pyhdl_stuff['gate_list'][2] == g3
        assert pyhdl_stuff['inputs']['a'] == a
        assert pyhdl_stuff['inputs']['b'] == b
        assert pyhdl_stuff['outputs']['d'] == d
        assert pyhdl_stuff['outputs']['e'] == e
        assert pyhdl_stuff['internals']['c'] == c
