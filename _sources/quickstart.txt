.. _quickstart:

Quickstart
============

Playing around with gates
-------------------------

You can create a gate in PyHDL like this::

    from pyhdl import Wire, NandGate
    a, b, out = Wire(), Wire(), Wire()
    gate = NandGate(a=a, b=b, out=out)

    a.val, b.val = '1', '1'
    gate.eval()
    print out.val # 0

So what did that code do?

1. First we import the :class:`~pyhdl.Wire` class. An instance of this class is a wire that carries a boolean value.
2. Then we import the :class:`~pyhdl.NandGate` class.
3. We then create three wires `a`, `b`, and `out`
4. Then, we create a Nand Gate, with 2 inputs `a` and `b`, and an output `out`
5. We then set the value of `a` and `b` to `'1'`
6. Since we modified the inputs of `gate`, we must run `gate.eval()` to update the gates outputs.
7. Finally, we print the output of the gate.
