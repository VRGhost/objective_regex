from . import base

class Text(base.RegexBase):
    """Matches plain text string."""

    def __init__(self, pattern):
        self.children = (pattern, )

class Raw(Text):
    """Raw regexp, does not escape magical chars."""

    def _getRegex(self, ctx=None):
        with ctx.processing(self):
            return self.joinChar.join(self.children)

# vim: set sts=4 sw=4 et :
