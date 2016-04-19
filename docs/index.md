# Welcome to PyHDL

PyHDL is a simple python based Hardware Description Language.

## Examples
```python
from pyhdl.declarative import Module
from pyhdl.wire import Wire
from pyhdl.primitives import NandGate


class NotGate(Module):
    a = Wire(type="input")
    out = Wire(type="output")
    gate1 = NandGate(a, a, out)


class OrGate(Module):
    a = Wire(type="input")
    b = Wire(type="input")
    temp1 = Wire(type="internal")
    temp2 = Wire(type="internal")
    out = Wire(type="output")
    gate1 = NandGate(a, a, temp1)
    gate2 = NandGate(b, b, temp2)
    gate3 = NandGate(temp1, temp2, out)


class XorGate(Module):
    a = Wire(type="input")
    b = Wire(type="input")
    temp1 = Wire(type="internal")
    temp2 = Wire(type="internal")
    temp3 = Wire(type="internal")
    out = Wire(type="output")
    gate1 = NandGate(a, b, temp1)
    gate2 = NandGate(a, temp1, temp2)
    gate3 = NandGate(temp1, b, temp3)
    gate4 = NandGate(temp2, temp3, out)


class AndGate(Module):
    a = Wire(type="input")
    b = Wire(type="input")
    temp = Wire(type="internal")
    out = Wire(type="output")
    gate1 = NandGate(a, b, temp)
    gate2 = NotGate(a=temp, out=out)
```