# Nand gate

## Truth table

| a | b | out |
|---|---|-----|
| 0 | 0 |  1  |
| 1 | 0 |  0  |
| 0 | 1 |  0  |
| 1 | 1 |  0  |

## Usage

```
>>> from pyhdl.primitives import NandGate
>>> a = Wire()
>>> b = Wire()
>>> out = Wire()
>>> gate = NandGate(a=a, b=b, out=out)
>>> a.set('1')
>>> b.set('1')
>>> a.get()
1
```