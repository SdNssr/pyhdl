# Wire

Wires are just circuit wires.

They have a fixed width and a type.

The type determines whether the wire is an output, an input or something else.

## Usage

```python
>>> from pyhdl.wire import Wire
>>> a = Wire(width=3,       # This determines the width of the wire in bits
>>>          type="input")  # This tells that the wire is an input. 
>>>                         # It could also be an output or a internal wire.
>>> a.val # This gets the value of the wire
'xxx'
>>> a.val = '101' # This sets the value of the wire
>>> a.val
'101'
>>> a.val = '12a' # If you try to set an invalid value,
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "pyhdl/wire.py", line 31, in val
    raise HDLError("Invalid value passed to wire: {0}".format(value))
pyhdl.utils.HDLError: Invalid value passed to wire: 121
>>> # You get an error
```

# Subwires

Sometimes, you need to take a subset of the wire. For example, you may only be interested in the second bit of the wire shown above.

You can use a subwire to do this.

```python
>>> b = a[2:3] # Take a subset of the wire a, from bits 2 to 3
>>> a.val = "111"
>>> b.val
1
>>> a.val = "101"
>>> b.val
0
```

**But do note, you can only take a subset of a wire once.**
