# And gate

## Truth table

| a | b | out |
|---|---|-----|
| 0 | 0 |  1  |
| 1 | 0 |  0  |
| 0 | 1 |  0  |
| 1 | 1 |  0  |

## Usage

```python
>>> from pyhdl.primitives import NandGate
>>> a = Wire()
>>> b = Wire()
>>> out = Wire()
>>> gate = NandGate(a=a, b=b, out=out)
>>> a.val = '1'
>>> b.val = '1'
>>> out.val
1
```