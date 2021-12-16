import functools
import itertools

class Context(object):
    """Structural node of a tree that represents regex parsing state"""

    _visited = _visiting = None
    strict = True

    def __init__(self, strict):
        self._visited = []
        self._visiting = []
        self.strict = strict
        self.processing = functools.partial(_CtxProcessingToken, self)

    def getVisited(self, filterBy=None):
        if not filterBy:
            filterBy = lambda el: True

        return itertools.ifilter(filterBy, self._visited)

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
