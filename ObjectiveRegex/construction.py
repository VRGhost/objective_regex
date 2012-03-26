import functools

class Context(object):
    """Structural node of a tree that represents regex parsing state"""

    _visited = _visiting = None

    def __init__(self):
        self._visited = []
        self._visiting = []
        self.processing = functools.partial(_CtxProcessingToken, self)

    def haveVisited(self, obj):
        return obj in self._visited

    @property
    def visited(self):
        return self._visited

class _CtxProcessingToken(object):

    def __init__(self, context, target):
        self.ctx = context
        self.target = target

    def __enter__(self):
        self.ctx._visiting.append(self.target)

    def __exit__(self, *tb):
        self.ctx._visiting.remove(self.target)
        self.ctx._visited.append(self.target)

# vim: set sts=4 sw=4
