# Defining your own gates

You can define your own gates using modules.

```python
>>> from pyhdl.wire import Wire
>>> from pyhdl.declarative import Module
>>> from pyhdl.primitives import NotGate, AndGate, OrGate, DFF

>>> class Multiplexer2(Module):
>>>     a = Wire(type='input')
>>>     b = Wire(type='input')
>>>     sel = Wire(type='input')

>>>     selinv = Wire()
>>>     a_and = Wire()
>>>     b_and = Wire()

>>>     out = Wire(type='output')

>>>     invsel = NotGate(a=sel, out=selinv)

>>>     amux = AndGate(a=a, b=sel, out=a_and)
>>>     bmux = AndGate(a=b, b=selinv, out=b_and)

>>>     muxor = OrGate(a=a_and, b=b_and, out=out)

>>> a = Wire()
>>> b = Wire()
>>> sel = Wire()
>>> out = Wire()

>>> mux = Multiplexer2(a=a, b=b, sel=sel, out=out)

>>> a.val = '1'
>>> b.val = '0'
>>> sel.val = '1'
>>> out.val
'1'

>>> sel.val = '0'
>>> out.val
'0'
```