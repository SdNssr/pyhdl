"""
    A composite gate.
    
    gates - A list of gates in topological order.
    outputs - The outputs of the gate. (For debugging)
    inputs - The inputs of the gate. (For debugging)
    internals - The internal wires of the gate. (For debugging)
    gateDict - 

"""

from pyhdl.gate import Gate

class Composite(Gate):

    def __init__(self, gates, inputs, outputs, internals, gateDict):
        self._input = inputs
        self._output = outputs
        self._internal = internals
        self.gates = gates
        self._gates = gateDict

    def tick(self):
        for gate in self.gates:
            gate.tick()

    def tock(self):
        for gate in self.gates:
            gate.tock()

    def eval(self):
        for gate in self.gates:
            gate.eval()

    def view(self, signal):
        if signal in self._input:
            return self._input[signal]
        elif signal in self._output:
            return self._output[signal]
        elif signal in self._internal:
            return self._internal[signal]
        elif signal in self._gates:
            return self._gates[signal]
        else:
            return None

    def __getattr__(self, signal):
        if self.view(signal):
            return self.view(signal)
        else:
            raise AttributeError("AttributeError")
