# form .

from . import base, types

class Any(base.RegexBase):

    joinChar = '|'

    def __init__(self, children):
        super(Any, self).__init__()

        self.children = tuple(children)

    def _getRegex(self, ctx):

        _mask = "(?({}){})"
        _patterns = [self.ifTrue ]

        if self.ifFalse:
            _mask = "(?({}){}|{})"
            _patterns.append(self.ifFalse)

        return _mask.format(
            self.cond.getName(ctx),
            *(
                _el._asHiddenGroup()._getRegex(ctx)
                for _el in _patterns
            )
        )

# vim: set sts=4 sw=4
