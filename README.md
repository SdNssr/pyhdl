# PyHDL

[![Travis CI](https://travis-ci.org/SdNssr/pyhdl.svg?branch=master)](https://travis-ci.org/SdNssr/pyhdl?branch=master)
[![codecov.io](https://codecov.io/github/SdNssr/pyhdl/coverage.svg?branch=master)](https://codecov.io/github/SdNssr/pyhdl?branch=master)
[![Join the chat at https://gitter.im/SdNssr/pyhdl](https://badges.gitter.im/SdNssr/pyhdl.svg)](https://gitter.im/SdNssr/pyhdl?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![PyPI version](https://badge.fury.io/py/pyhdl.svg)](https://badge.fury.io/py/pyhdl)
[![PyPI](https://img.shields.io/pypi/dm/pyhdl.svg?maxAge=2592000)]()
[![License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)]()

A simple HDL written in Python.

```python
from pyhdl import Wire, NandGate
a, b, out = Wire(), Wire(), Wire()
gate = NandGate(a=a, b=b, out=out)

a.val, b.val = '1', '1'
gate.eval()
print out.val # 0
```

You can read the docs at http://pyhdl.sdnssr.me.