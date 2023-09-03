stream")

    def __init__(self, process, stream_name):
        self._proc = process
        self._stream = getattr(process, stream_name)

    def __getattr__(self, attr):
        return getattr(self._stream, attr)


class Traversable(object):

    """Simple interface to perform depth-first or breadth-first traversals
    