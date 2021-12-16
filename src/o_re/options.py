from . import base


class OptionBase(base.RegexBase):

    wrap = "???I AM OPTION {!r}????"

    def __init__(self, child):
        super(OptionBase, self).__init__()
        self.children = (child, )

    def _get_regex(self, ctx):
        return self.wrap.format(super()._get_regex(ctx))


class Optional(OptionBase):

    wrap = "{}?"


class AnyNumber(OptionBase):
    wrap = "{}*"


class NonZeroCount(OptionBase):
    wrap = "{}+"
