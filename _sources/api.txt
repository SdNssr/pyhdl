.. _api:

API
===

.. module:: pyhdl

This part of the documentation covers all the interfaces of PyHDL.


Simulator
------------------

.. autoclass:: Simulator
   :members:
   :inherited-members:


Wire
-----------------

.. autoclass:: Wire
   :members:
   :inherited-members:


SubWire
-----------------

.. autoclass:: SubWire
   :members:
   :inherited-members:


ConstantWire
-------------------

.. autoclass:: ConstantWire
   :members:
   :inherited-members:

Gate
-------------------

.. autoclass:: Gate
   :members:
   :inherited-members:

Simple combinatorial gates
--------------------------

Named parameters from ``a`` to ``z`` are used as inputs, and ``out`` is used as the output.
(Except in the case of the not gate, where ``inp`` is used as the input.)

``width`` is used to specify the width of the inputs, and ``ways`` is used to specify the arity of the gate.

For example:::

   from pyhdl import NandGate, Wire
   a, b, c, out = Wire(), Wire(), Wire(), Wire()
   gate = NandGate(a=a, b=b, c=c, out=out, ways=3)

.. autoclass:: NandGate
   :members:
   :inherited-members:


.. autoclass:: AndGate
   :members:
   :inherited-members:


.. autoclass:: NorGate
   :members:
   :inherited-members:


.. autoclass:: OrGate
   :members:
   :inherited-members:


.. autoclass:: XorGate
   :members:
   :inherited-members:

.. autoclass:: NotGate
   :members:
   :inherited-members:


Multiplexer
------------------

.. autoclass:: Multiplexer
   :members:
   :inherited-members:


Demultiplexer
--------------------

.. autoclass:: Demultiplexer
   :members:
   :inherited-members:


HalfAdder
-----------------

.. autoclass:: HalfAdder
   :members:
   :inherited-members:


FullAdder
-----------------

.. autoclass:: FullAdder
   :members:
   :inherited-members:


Adder
-----------------

.. autoclass:: Adder
   :members:
   :inherited-members:


DFF
-----------------

.. autoclass:: DFF
   :members:
   :inherited-members:


Register
-----------------

.. autoclass:: Register
   :members:
   :inherited-members:


Memory
-----------------

.. autoclass:: Memory
   :members:
   :inherited-members:
