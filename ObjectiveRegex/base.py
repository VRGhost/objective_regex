import re
import functools


from . import construction

class RegexBase(object):

    # List of characters that should be escaped in this particular regexp
    escapeChars = ('\\', '.', '^', '$', '*', '+', '{', '}', '?', '[', ']', '|', '(', ')')

    # List of children regex (or text) object
    children = ()
    # Char that is used to join children regex representations.
    joinChar = ''

    def getRegex(self):
        """Return the text regexp representation"""
        _ctx = construction.Context()
        return self._getRegex(_ctx)

    def getCompiled(self, flags=0):
        """Return compiled regex object. """
        return re.compile(self.getRegex(), flags)

    def escape(self, text):
        """Escape given text string."""
        for _el in self.escapeChars:
            text = text.replace(_el, '\\'+_el)
        return text


    def append(self, *others):
        from .groups import HiddenGroup
        _grp = self._toHiddenGroup

        _out = [_grp(self)]
        _out.extend(_grp(_el) for _el in others)
        return HiddenGroup(_out)

    def asGroup(self, name=None):
        """ Return given regexp as group. If `name` parameter is passed, than named group is created. Otherwise the id-numbered group is used."""
        from . import groups
        if name:
            _rv = groups.NamedGroup((self,), name)
        else:
            _rv = groups.Group((self, ))
        return _rv

    @property
    def times(self):
        try:
            return self.__timesCache
        except AttributeError:
            self.__timesCache = _rv = _TimesObject(self)
            return _rv

    def _getRegex(self, ctx):
        """Actual regexp construction function."""
        _parts = []

        with ctx.processing(self):
            for _child in self.children:
                try:
                    _text = _child._getRegex(ctx)
                except AttributeError:
                    _text = self.escape(str(_child))

                _parts.append(_text)

        return self.joinChar.join(_parts)


    def _asHiddenGroup(self):
        """Return this regexp as group that does not appear in the match results."""
        return self._toHiddenGroup(self)

    def _toHiddenGroup(self, obj):
        if getattr(obj, "isGroup", False):
            return obj
        else:
            from . import groups
            return groups.HiddenGroup((obj, ))

    __mul__ = lambda s, oth: s.times(oth)
    __add__ = lambda s, oth: s.append(oth)

    def __str__(self):
        return self.getRegex()

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.getRegex())


class _TimesObject(object):

    def __init__(self, regex):
        self.reg = regex
        from . import repeats, options
        self.rep = repeats
        self.opt = options

    def repeated(self, *args, **kwargs):
        """This regexp repeated given number of times."""
        return self.rep.RepeatBorders(self._trg, *args, **kwargs)

    def maybe(self):
        """Return regexp that matches if this regexp ether matches or not."""
        return self.opt.Optional(self._trg)

    def any(self):
        """Return regexp that matches if this regexp matches any number of times."""
        return self.opt.AnyNumber(self._trg)

    def some(self):
        """Return regexp that matches if this regexp matches non-zero number of times."""
        return self.opt.NonZeroCount(self._trg)

    def __call__(self, num):
        return self.rep.Times(self._trg, num)

    @property
    def _trg(self):
        return self.reg._asHiddenGroup()

# vim: set sts=4 sw=4 et :
