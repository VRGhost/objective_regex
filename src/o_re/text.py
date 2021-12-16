from . import base, types


class Text(base.RegexBase):
    """Matches plain text string."""

    type = types.RegexType.Text
    # List of characters that should be escaped in this particular regexp
    escape_chars = ('.', '^', '$', '*', '+', '{', '}', '?', '[', ']', '|', '(', ')')

    def __init__(self, pattern):
        super(Text, self).__init__()
        self.pattern = pattern

    def _get_regex(self, ctx):
        with ctx.processing(self):
            return self.escape(self.pattern, self.escape_chars)

    def __eq__(self, other):
        return super().__eq__(other) and (self.get_regex() == other.get_regex())


class Raw(Text):
    """Raw regexp, does not escape magical chars."""

    type = types.RegexType.Raw

    def _get_regex(self, ctx):
        with ctx.processing(self):
            return self.pattern
