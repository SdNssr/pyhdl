"""
    A circuit wire.
"""
from pyhdl.utils import *


class Wire(object):

    allowed = set('01xX')

    def __init__(self, width=1, type="undefined"):
        self._width = width
        self._value = width * 'x'
        self._msb = 1 << (self._width - 1)
        self._max = (1 << self._width) - 1

        self._format_trunc = '0>{}b'.format(self._width - 1)
        self._format = '0>{}b'.format(self._width)

        self.type = type

        self._listeners = []
        self._driver = None

    @property
    def val(self):
        return self._value

    @val.setter
    def val(self, value):
        if (set(value) <= self.allowed) or (len(value) != self._width):
            self._value = value
            for listener in self._listeners:
                listener.eval()
        else:
            raise HDLError("Invalid value passed to wire: {0}".format(value))

    @property
    def uival(self):
        return int(self._value, 2)

    @uival.setter
    def uival(self, val):
        self._value = format(val, self._format)[-self._width:]

    @property
    def ival(self):
        msb = self._msb if self._value[0] == '1' else 0
        val = int(self._value[1:], 2)
        return val - msb

    @ival.setter
    def ival(self, value):
        if value == 0:
            self._value = '0' * self._width
        elif (value/abs(value)) == 1:
            truncated = value % (self._msb - 1)
            self._value = '0' + format(truncated, self._format_trunc)[-(self._width-1):]
        else:
            truncated = value % (self._msb)
            self._value = '1' + format(truncated, self._format_trunc)[-(self._width-1):]

        for listener in self._listeners:
                listener.eval()

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        if self._driver is None:
            self._driver = driver
        else:
            raise HDLError("More than 1 driver on net.")

    @property
    def listeners(self):
        return self._listeners

    def addListener(self, listener):
        self._listeners.append(listener)

    def __len__(self):
        return self._width

    def __getitem__(self, key):
        return SubWire(self, key)

    def __iter__(self):
        for i in range(0, self._width):
            yield slice(i, i + 1)

    def __contains__(self, key):
        if key.stop > self._width:
            return False
        else:
            return True


class SubWire(object):

    def __init__(self, node, sub, type="undefined"):
        self.node = node
        self.type = type
        self.sub = sub
        self._listeners = []
        self.node.addListener(self)

    @property
    def val(self):
        return self.node.val[self.sub]

    @property
    def ival(self):
        msb = self._msb if self.val[0] == '1' else 0
        val = int(self.val[1:], 2)
        return val - msb

    @property
    def uival(self):
        return int(self.val, 2)

    def addListener(self, listener):
        self._listeners.append(listener)

    def eval(self):
        for listener in self._listeners:
            listener.eval()

    @property
    def driver(self):
        return self.node.driver

    @property
    def listeners(self):
        return self._listeners


class BridgeWire(object):
    """
        A bridge wire from node1 to node2.

        Update node2 when node1 changes.
    """

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.node1.addListener(self)
        self.node2.driver = self

    def eval(self):
        self.node2.val = self.node1.val
