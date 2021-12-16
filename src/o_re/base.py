import re

from . import construction, types


class RegexBase(object):

    # List of children regex (or text) object
    children = ()
    # Char that is used to join children regex representations.
    type = types.RegexType.Unknown

    times = None

    def __init__(self):
        super(RegexBase, self).__init__()
        self.times = _TimesObject(self)

    def get_regex(self, strict=True):
        """Return the text regexp representation

        If `strict` is True, than in case of construction error is detected, an exception should be raised.
        Otherwise, the object is expected to return a string (but it is not expected to be a correct regex).
        """
        _ctx = construction.Context(strict=strict)
        return self._get_regex(_ctx)

    def get_compiled(self, flags=0):
        """Return compiled regex object. """
        return re.compile(self.get_regex(), flags)

    def escape(self, text, escape_chars):
        """Escape given text string."""
        _bs = '\\'
        # backslash is always escaped
        text = text.replace(_bs, _bs*2)
        for _el in escape_chars:
            assert _el != _bs, "Backslash has been already escaped"
            text = text.replace(_el, _bs + _el)
        return text

    def append(self, *others):
        from .groups import HiddenGroup

        def _grp(obj):
            return self._to_hidden_group(obj, True)

        _out = [_grp(self)]
        _out.extend(_grp(_el) for _el in others)
        return HiddenGroup(_out)

    def prepend(self, *others):
        from .groups import HiddenGroup

        def _grp(obj):
            return self._to_hidden_group(obj, True)

        _out = [_grp(_el) for _el in others]
        _out.append(_grp(self))
        return HiddenGroup(_out)

    def as_group(self, name=None):
        """Return given regexp as group.

        If `name` parameter is passed, than named group is created. Otherwise the id-numbered group is used.
        """
        from . import groups
        if name:
            _rv = groups.NamedGroup((self,), name)
        else:
            _rv = groups.Group((self, ))
        return _rv

    def _get_regex(self, ctx):
        """Actual regexp construction function."""
        _parts = []

        with ctx.processing(self):
            for _child in self.children:
                _parts.append(self._as_regex_obj(_child)._get_regex(ctx))
        return ''.join(_parts)

    def _as_hidden_group(self):
        """Return this regexp as group that does not appear in the match results."""
        return self._to_hidden_group(self)

    def _to_hidden_group(self, obj, force_cls=False):
        _obj = self._as_regex_obj(obj)
        if _obj.type & types.RegexType.Group:
            if not force_cls or (force_cls and types.RegexType.HiddenGroup.implemented_by(_obj.type)):
                return obj
        # else
        from . import groups
        return groups.HiddenGroup((_obj, ))

    def _as_regex_obj(self, target):
        _is_regex = False
        try:
            _hndl = target.type
        except AttributeError:
            pass
        else:
            _is_regex = isinstance(_hndl, types.RegexType)

        if _is_regex:
            _rv = target
        else:
            from . import text
            _rv = text.Text(target)
        return _rv

    def __mul__(self, other):
        return self.times(other)

    def __add__(self, other):
        return self.append(other)

    def __radd__(self, other):
        return self.prepend(other)

    def __str__(self):
        return self.get_regex()

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.get_regex(strict=False))

    def __eq__(self, other):
        return self.type == other.type and self.children == other.children


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

    def many(self):
        """Return regexp that matches if this regexp matches non-zero number of times."""
        return self.opt.NonZeroCount(self._trg)

    def __call__(self, num):
        return self.rep.Times(self._trg, num)

    @property
    def _trg(self):
        return self.reg._as_hidden_group()
