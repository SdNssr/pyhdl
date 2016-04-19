# D flip flop

A D flip flop samples it's inputs on every tick, and sets it's outputs on every tock.

## Example

```python
>>> from pyhdl.primitives import DFF
>>> input = Wire()
>>> output = Wire()
>>> flipflop = DFF(input=input, output=output, default='0')
>>> output.val
0
>>> input.set('1')
>>> flipflop.tick()
>>> output.val
'x'
>>> input.val = '0'
>>> flipflop.tock()
>>> output.val
'1'
```