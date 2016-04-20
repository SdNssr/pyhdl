# Welcome to PyHDL

PyHDL is a simple python based Hardware Description Language.

```python
from pyhdl import Wire, AndGate

a, b, out = Wire(), Wire(), Wire()
gate = AndGate(a=a, b=b, out=out)
a.val, b.val = '1', '1'
print out.val # '1'
```
