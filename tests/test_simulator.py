from pyhdl.simulator import Simulator, flatten_list
import unittest


def test_flatten_list():
    nested = [
        1,
        2,
        [
            3,
            4,
            [
                5,
                [
                    6,
                ],
                7
            ],
            8
        ],
        9
    ]

    flat = list(range(1, 10))

    assert flatten_list(nested) == flat
    assert flatten_list(flat) == flat


class GateSimulator(object):

    def __init__(self, name, evals, ticks, tocks):
        self.name = name
        self.evals = evals
        self.ticks = ticks
        self.tocks = tocks

    def eval(self):
        self.evals.append(self.name)
    
    def tick(self):
        self.ticks.append(self.name)

    def tock(self):
        self.tocks.append(self.name)


class TestSimulator(unittest.TestCase):

    def setUp(self):
        self.evals = []
        self.ticks = []
        self.tocks = []

        self.gates = [
            GateSimulator(1, self.evals, self.ticks, self.tocks),
            GateSimulator(2, self.evals, self.ticks, self.tocks),
            [
                GateSimulator(3, self.evals, self.ticks, self.tocks),
                GateSimulator(4, self.evals, self.ticks, self.tocks),
                [
                    GateSimulator(5, self.evals, self.ticks, self.tocks),
                    [
                        GateSimulator(6, self.evals, self.ticks, self.tocks),
                    ],
                    GateSimulator(7, self.evals, self.ticks, self.tocks)
                ],
                GateSimulator(8, self.evals, self.ticks, self.tocks)
            ],
            GateSimulator(9, self.evals, self.ticks, self.tocks)
        ]

        self.simulator = Simulator(self.gates)

    def test_tick(self):
        self.simulator.tick()
        self.assertEqual(self.ticks, list(range(1, 10)))

    def test_tock(self):
        self.simulator.tock()
        self.assertEqual(self.tocks, list(range(1, 10)))

    def test_eval(self):
        self.simulator.eval()
        self.assertEqual(self.evals, list(range(1, 10)))
