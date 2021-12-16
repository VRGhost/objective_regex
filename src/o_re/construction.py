import functools


class Context(object):
    """Structural node of a tree that represents regex parsing state"""

    _visited = _visiting = None
    strict = True

    def __init__(self, strict):
        self._visited = []
        self._visiting = []
        self.strict = strict
        self.processing = functools.partial(_CtxProcessingToken, self)

    def get_visited(self, filter_by=None):
        if not filter_by:
            def filter_by(el):
                return True

        return (el for el in self._visited if filter_by(el))


class _CtxProcessingToken(object):

    def __init__(self, context, target):
        self.ctx = context
        self.target = target

    def __enter__(self):
        self.ctx._visiting.append(self.target)

    def __exit__(self, *tb):
        self.ctx._visiting.remove(self.target)
        self.ctx._visited.append(self.target)
