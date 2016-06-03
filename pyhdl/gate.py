"""
    An abstract gate class.
    tick() - Run on every tick.
    tock() - Run on every tock.
    eval() - Run when input changes.
    view(signal) - View signal
"""


class Gate(object):

    def tick():
        """
            Run on every tick.
        """
        raise NotImplementedError('Abstract method tick called.')

    def tock():
        """
            Run on every tock.
        """
        raise NotImplementedError('Abstract method tick called.')

    def eval():
        """
            Run eval to update the gate's outputs whenever you change the inputs.
        """
        raise NotImplementedError('Abstract method tick called.')

    def view(signal):
        """
            View the signal ``signal``.

            :param signal: The signal to view.
            :type signal: str
        """
        raise NotImplementedError('Abstract method tick called.')
