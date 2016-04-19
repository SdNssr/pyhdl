"""
    Declarative way to specify composite classes.
"""

import copy
import itertools
from gate import Gate
from wire import Wire, SubWire, BridgeWire
from composite import Composite
from utils import HDLError


class ModuleMetaClass(type):

    def __new__(cls, classname, bases, dict_):

        gates = {}

        inputs = {}
        outputs = {}
        internals = {}

        gate_graph = {}

        # Assemble gates
        for attr, value in dict_.iteritems():
            if isinstance(value, Gate):
                gates[attr] = value

        gate_names = {value: key for key, value in gates.items()}

        # Assemble wires
        for attr, value in dict_.iteritems():
            if isinstance(value, Wire) or isinstance(value, SubWire):
                # Add wire to inputs, outputs or internals
                if value.type == "input":
                    inputs[attr] = value
                elif value.type == "output":
                    outputs[attr] = value
                else:
                    internals[attr] = value

                # Assemble DAG
                driver = value.driver
                if driver in gate_names:
                    listeners = [gate_names[x] for x in value.listeners if x in gate_names]
                    if driver in gate_graph:
                        gate_graph[gate_names[driver]] += listeners
                    else:
                        gate_graph[gate_names[driver]] = listeners

        dict_['_pyhdl_stuff'] = {}
        dict_['_pyhdl_stuff']['gates'] = gates
        dict_['_pyhdl_stuff']['gate_list'] = [gates[x] for x in cls.topological_sort(gate_graph)]
        dict_['_pyhdl_stuff']['inputs'] = inputs
        dict_['_pyhdl_stuff']['outputs'] = outputs
        dict_['_pyhdl_stuff']['internals'] = internals

        return type.__new__(cls, classname, bases, dict_)

    @classmethod
    def topological_sort(cls, graph):
        sorted_graph = []

        names = set(graph.keys())
        connected = set(itertools.chain.from_iterable(graph.values()))
        start = names - connected

        while len(start) != 0:
            n = start.pop()
            sorted_graph.append(n)

            del graph[n]

            names = set(graph.keys())
            connected = set(itertools.chain.from_iterable(graph.values()))
            start = names - connected

        if any([x for x in graph]):
            raise HDLError('Non acyclic Module')

        return sorted_graph


class Module(object):
    __metaclass__ = ModuleMetaClass

    def __new__(cls, **kwargs):
        stuff = copy.deepcopy(cls._pyhdl_stuff)
        gates = stuff['gate_list']
        inputs = stuff['inputs']
        outputs = stuff['outputs']
        internals = stuff['internals']
        gateDict = stuff['gates']

        for arg in kwargs:
            if arg in inputs:
                BridgeWire(kwargs[arg], inputs[arg])
            elif arg in outputs:
                BridgeWire(outputs[arg], kwargs[arg])

        return Composite(gates, inputs, outputs, internals, gateDict)

