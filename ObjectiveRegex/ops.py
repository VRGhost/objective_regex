# form .

from . import base, types

class Any(base.RegexBase):

    joinChar = '|'

    def __init__(self, children):
        super(Any, self).__init__()

        self.children = tuple(children)

    def _getRegex(self, ctx):
        return "|".join(
            self._toHiddenGroup(_el)._getRegex(ctx)
            for _el in self.children
        )

# vim: set sts=4 sw=4