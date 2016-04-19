# D flip flop

A D flip flop samples it's inputs on every tick, and sets it's outputs on every tock.

## Example

```
>>> from pyhdl.primitives import DFF
>>> input = Wire()
>>> output = Wire()
>>> flipflop = DFF(input=input, output=output)
>>> input.set('1')
>>> flipflop.tick()
>>> output.val
'x'
>>> input.val = '0'
>>> flipflop.tock()
>>> output.val
'1'
```