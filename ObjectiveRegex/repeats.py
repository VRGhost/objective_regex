from . import base


class RepeatBase(base.RegexBase):
    """Base class for all repeat objects."""

class Times(RepeatBase):

    count = 0

    def __init__(self, target, count):
        self.children = (target, )
        self.count = count

        if count <= 0 or int(count) != count:
            raise RuntimeError("Repeat count is only allowed to be positive integer.")

    def _getRegex(self, ctx):
        return "{regex}{{{times}}}".format(
            regex=super(Times, self)._getRegex(ctx),
            times=self.count,
        )

class RepeatBorders(RepeatBase):
    """Repeats target object several times."""

    max = min = lazy = ''

    def __init__(self, target, min=-1, max=-1, lazy=False):
        super(RepeatBorders, self).__init__()
        self.children = (target, )
        self.lazy = '?' if lazy else ''

        def _toLimit(cond):
            if not cond:
                if cond == 0:
                    return 0
                else:
                    return ''
            elif cond < 0:
                return ''
            else:
                return cond

        _max = _toLimit(max)
        _min = _toLimit(min)

        if not any(_el and _el > 0 for _el in (_max, _min)):
            raise RuntimeError("Wrong number of repeats: max={!r}, min={!r}".format(max, min))

        self.max = _max
        self.min = _min

    def _getRegex(self, ctx):
        return "{regex}{{{min}, {max}}}{lazy}".format(
            regex=super(RepeatBorders, self)._getRegex(ctx),
            min=self.min,
            max=self.max,
            lazy=self.lazy,
        )

# vim: set sts=4 sw=4 et :
