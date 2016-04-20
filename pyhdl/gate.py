"""
    An abstract gate class.
    tick() - Run on every tick.
    tock() - Run on every tock.
    eval() - Run when input changes.
    view(signal) - View signal
"""


class Gate(object):

    def register(self, *inputs):
        for input in inputs:
            input.addListener(self)

    def register_output(self, *outputs):
        for output in outputs:
            output.driver = self
