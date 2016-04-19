# Not gate

## Truth table

| a | out |
|---|-----|
| 0 |  1  |
| 1 |  0  |

## Usage

```
>>> from pyhdl.primitives import NotGate
>>> a = Wire()
>>> out = Wire()
>>> gate = NotGate(a=a, out=out)
>>> a.val = '1'
>>> out.val
0
```