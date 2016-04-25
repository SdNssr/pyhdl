from pyhdl.wire import Wire, SubWire, BridgeWire
from pyhdl.utils import HDLError
import unittest


class TestWire(unittest.TestCase):

    def setUp(self):
        self.wire = Wire()

    def test_default(self):
        assert self.wire.val == 'x'

    def set_val(self, x):
        self.wire.val = x
        assert self.wire.val == x

    def test_set(self):
        self.set_val('x')
        self.set_val('X')
        self.set_val('0')
        self.set_val('1')

        with self.assertRaises(HDLError) as cm:
            self.wire.val = 'A'

    def test_listeners(self):
        self.wire.addListener('a')
        assert self.wire.listeners == ['a']

    def test_driver(self):
        self.wire.driver = 'abc'
        assert self.wire.driver == 'abc'

    def test_multiple_driver(self):
        with self.assertRaises(HDLError) as cm:
            self.wire.driver = 'abc'
            self.wire.driver = 'xyz'


class TestWireMulti(unittest.TestCase):

    def setUp(self):
        self.wire = Wire(width=3)

    def test_default(self):
        assert self.wire.val == 'xxx'

    def set_val(self, x):
        self.wire.val = x
        assert self.wire.val == x

    def test_set(self):
        self.set_val('xxx')
        self.set_val('01x')
        self.set_val('111')
        self.set_val('00X')
        self.set_val('110')
        self.set_val('001')

        with self.assertRaises(HDLError) as cm:
            self.wire.val = 'ABC'


class TestWireIval(unittest.TestCase):

    def setUp(self):
        self.wire = Wire(width=16)

    def test_default(self):
        assert self.wire.val == 'x' * 16

    def set_ival(self, x):
        self.wire.ival = x
        self.assertEqual(self.wire.ival, x)

    def test_set(self):
        self.set_ival(123)
        self.set_ival(435)
        self.set_ival(-452)
        self.set_ival(23458)
        self.set_ival(-23458)


class TestSubWire(unittest.TestCase):

    def setUp(self):
        self.wire = Wire(width=4)
        self.subwire = SubWire(self.wire, slice(2, 3))
        self.evalCalls = 0

    def eval(self):
        self.evalCalls += 1

    def test_default(self):
        assert self.subwire.val == 'x'

    def set_val(self, x):
        self.wire.val = '01{0}1'.format(x)
        assert self.subwire.val == x

    def test_set(self):
        self.set_val('x')
        self.set_val('X')
        self.set_val('0')
        self.set_val('1')

    def test_listeners(self):
        self.subwire.addListener('a')
        assert self.subwire.listeners == ['a']

    def test_driver(self):
        self.wire.driver = 'abc'
        assert self.subwire.driver == 'abc'

    def test_eval(self):
        self.subwire.addListener(self)
        self.subwire.eval()
        assert self.evalCalls == 1


class TestSubWireSlice(unittest.TestCase):

    def setUp(self):
        self.wire = Wire(width=4)
        self.subwire = self.wire[2:3]
        self.evalCalls = 0

    def eval(self):
        self.evalCalls += 1

    def test_default(self):
        assert self.subwire.val == 'x'

    def set_val(self, x):
        self.wire.val = '01{0}1'.format(x)
        assert self.subwire.val == x

    def test_set(self):
        self.set_val('x')
        self.set_val('X')
        self.set_val('0')
        self.set_val('1')

    def test_listeners(self):
        self.subwire.addListener('a')
        assert self.subwire.listeners == ['a']

    def test_driver(self):
        self.wire.driver = 'abc'
        assert self.subwire.driver == 'abc'

    def test_eval(self):
        self.subwire.addListener(self)
        self.subwire.eval()
        assert self.evalCalls == 1

    def test_contains(self):
        assert slice(2, 3) in self.wire
        assert slice(10, 12) not in self.wire
        assert slice(0, 2) in self.wire

    def test_iter(self):
        i = 0
        for item in self.wire.__iter__():
            assert item == slice(i, i + 1)
            i += 1

    def test_len(self):
        assert len(self.wire) == 4


class TestBridgeWire(unittest.TestCase):

    def setUp(self):
        self.input = Wire()
        self.output = Wire()
        self.bridge = BridgeWire(self.input, self.output)

    def test_default(self):
        assert self.output.val == 'x'

    def set_val(self, x):
        self.input.val = x
        assert self.output.val == x

    def test_set(self):
        self.set_val('x')
        self.set_val('X')
        self.set_val('0')
        self.set_val('1')
