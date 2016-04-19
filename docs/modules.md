# Defining your own gates

You can define your own gates using modules.

```python
>>> from pyhdl.wire import Wire
>>> from pyhdl.declarative import Module
>>> from pyhdl.primitives import NandGate
>>> 
>>> # We are going to make a 3 input Nand Gate
>>> class NandGate3(Module):
>>>     a = Wire(type='input')
>>>     b = Wire(type='input')
>>>     c = Wire(type='input')
>>>     temp = Wire()
>>>     out = Wire(type='output')
>>>     nand1 = NandGate(a=a, b=b, out=temp)
>>>     nand2 = NandGate(a=temp, b=c, out=out)
>>> 
>>> # You can use it as a normal gate
>>> a = Wire()
>>> b = Wire()
>>> c = Wire()
>>> out = Wire()
>>> gate = NandGate3(a=a, b=b, c=c, out=out)
>>> a.val = '1'
>>> b.val = '1'
>>> c.val = '1'
>>> out.val
'0'
>>> c.val = '0'
>>> out.val
'1'
```