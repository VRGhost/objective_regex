from . import base


class Any(base.RegexBase):

    join_char = '|'

    def __init__(self, children):
        super(Any, self).__init__()
        self.children = tuple(children)

    def _get_regex(self, ctx):
        return self.join_char.join(
            self._to_hidden_group(_el)._get_regex(ctx)
            for _el in self.children
        )
