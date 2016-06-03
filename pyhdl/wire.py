"""
    A circuit wire.
"""
from pyhdl.utils import *


class Wire(object):
    """
        An arbitrary width wire.

        :param width: The width of the wire.
        :type width: int
        :param type: An arbitrary string to tag a wire. (DEPRECATED)
        :type type: str
    """

    allowed = set('01xX')

    def __init__(self, width=1, type="undefined"):
        self._width = width
        self._value = width * 'x'
        self._msb = 1 << (self._width - 1)
        self._max = (1 << self._width) - 1

        self._format_trunc = '0>{}b'.format(self._width - 1)
        self._format = '0>{}b'.format(self._width)

        self.type = type

    @property
    def val(self):
        """
            The binary value of a wire.
        """
        return self._value

    @val.setter
    def val(self, value):
        if (set(value) <= self.allowed) or (len(value) != self._width):
            self._value = value
        else:
            raise HDLError("Invalid value passed to wire: {0}".format(value))

    @property
    def uival(self):
        """
            The (unsigned) integer value of the wire.
        """
        return int(self._value, 2)

    @uival.setter
    def uival(self, val):
        self._value = format(val, self._format)[-self._width:]

    @property
    def ival(self):
        """
            The two's complement value of the wire.
        """
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


class ConstantWire(object):
    """
        A wire with a constant value.

        :param value: The (binary) value of the wire.
        :type value: str
        :param width: The width of the wire.
        :type width: int
        :param type: An arbitrary string to tag a wire. (DEPRECATED)
        :type type: str
    """

    def __init__(self, value, width=1, type="undefined"):
        self._width = width
        self._value = value
        self._msb = 1 << (self._width - 1)

        self.type = type

    @property
    def val(self):
        """
            The binary value of the wire.
        """
        return self._value

    @property
    def uival(self):
        """
            The (unsigned) integer value of the wire.
        """
        return int(self._value, 2)

    @property
    def ival(self):
        """
            The two's complement value of the wire.
        """
        msb = self._msb if self._value[0] == '1' else 0
        val = int(self._value[1:], 2)
        return val - msb

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
    """
        A slice of a wire.

        You can index into a wire using standard array notation to create a slice. e.g:

        >>> from pyhdl import ConstantWire
        >>> a = ConstantWire(value="010101", width=6)
        >>> b = a[0]
        >>> b.val
        "0"
        >>> c = a[0:2]
        >>> c.val
        "01"

        :param node: The wire you want to slice.
        :param sub: The slice you want to take.
        :param type: An arbitrary string to tag a wire. (DEPRECATED)
        :type type: str
    """

    def __init__(self, node, sub, type="undefined"):
        self.node = node
        self.type = type
        self.sub = sub

    @property
    def val(self):
        """
            The binary value of the wire.
        """
        return self.node.val[self.sub]

    @val.setter
    def val(self, val):
        l = list(self.node.val) 
        l[self.sub] = val
        self.node.val = ''.join(l)

    @property
    def ival(self):
        """
            The two's complement value of the wire.
        """
        msb = self._msb if self.val[0] == '1' else 0
        val = int(self.val[1:], 2)
        return val - msb

    @property
    def uival(self):
        """
            The (unsigned) integer value of the wire.
        """
        return int(self.val, 2)

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
