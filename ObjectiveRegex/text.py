from . import base, types

class Text(base.RegexBase):
    """Matches plain text string."""

    type = types.Text()
    # List of characters that should be escaped in this particular regexp
    escapeChars = ('.', '^', '$', '*', '+', '{', '}', '?', '[', ']', '|', '(', ')')

    def __init__(self, pattern):
        super(Text, self).__init__()
        self.pattern = pattern

    def _getRegex(self, ctx):
        with ctx.processing(self):
            return self.escape(self.pattern)

class Raw(Text):
    """Raw regexp, does not escape magical chars."""

    type = types.Raw()

    def _getRegex(self, ctx):
        with ctx.processing(self):
            return self.pattern

# vim: set sts=4 sw=4 et :
