from . import base, types


class If(base.RegexBase):

    type = types.RegexType.Group

    cond = if_true = if_false = None

    def __init__(self, cond, if_true, if_false=None):
        super(If, self).__init__()

        self.cond = cond
        self.if_true = if_true
        self.if_false = if_false
        self.children = (cond, if_true, if_false)

    def _get_regex(self, ctx):

        _mask = "(?({}){})"
        _patterns = [self.if_true]

        if self.if_false:
            _mask = "(?({}){}|{})"
            _patterns.append(self.if_false)

        return _mask.format(
            self.cond.get_name(ctx),
            *(
                self._to_hidden_group(_el)._get_regex(ctx)
                for _el in _patterns
            )
        )
