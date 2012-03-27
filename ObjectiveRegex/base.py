import re
import functools


from . import construction, types

class RegexBase(object):

    escapeChars = ()
    # List of children regex (or text) object
    children = ()
    # Char that is used to join children regex representations.
    type = types.BaseType()

    times = None

    def __init__(self):
        super(RegexBase, self).__init__()
        self.times = _TimesObject(self)

    def getRegex(self, strict=True):
        """Return the text regexp representation

        If `strict` is True, than in case of construction error is detected, an exception should be raised.
        Otherwise, the object is expected to return a string (but it is not expected to be a correct regex).
        """
        _ctx = construction.Context(strict=strict)
        return self._getRegex(_ctx)

    def getCompiled(self, flags=0):
        """Return compiled regex object. """
        return re.compile(self.getRegex(), flags)

    def escape(self, text):
        """Escape given text string."""
        _bs = '\\'
        # backslash is always escaped
        text = text.replace(_bs, _bs*2)
        for _el in self.escapeChars:
            assert _el != _bs, "Backslash has been already escaped"
            text = text.replace(_el, _bs + _el)
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

    def _getRegex(self, ctx):
        """Actual regexp construction function."""
        _parts = []

        with ctx.processing(self):
            for _child in self.children:
                _parts.append(self._asRegexObj(_child)._getRegex(ctx))
        return ''.join(_parts)


    def _asHiddenGroup(self):
        """Return this regexp as group that does not appear in the match results."""
        return self._toHiddenGroup(self)

    def _toHiddenGroup(self, obj):
        if obj.type.isGroup():
            return obj
        else:
            from . import groups
            return groups.HiddenGroup((self._asRegexObj(obj), ))

    def _asRegexObj(self, target):
        _isRegex = False
        try:
            _hndl = target.type
        except AttributeError:
            pass
        else:
            _isRegex = _hndl.isRegex()

        if _isRegex:
            _rv = target
        else:
            from . import text
            _rv = text.Text(target)
        return _rv

    __mul__ = lambda s, oth: s.times(oth)
    __add__ = lambda s, oth: s.append(oth)

    def __str__(self):
        return self.getRegex()

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.getRegex(strict=False))


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
