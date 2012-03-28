"""Class for regex objects to be able to declare regex type"""

class BaseType(object):
    """Base regex."""

    isRegex = lambda s: True

    def __getattr__(self, name):
        if name.startswith("is"):
            # By default, answer 'False' to all unknown 'is<Something>' requests
            _rv = lambda: False
        else:
            _rv = super(BaseType, self).__getattr__(name)

        setattr(self, name, _rv)
        return _rv

    def getTypes(self):
        try:
            return self.__typeCache
        except AttributeError:
            _out = []
            for _name in dir(self):
                if _name.startswith("is"):
                    _func = getattr(self, _name)
                    if _func():
                        _out.append(_name)
            self.__typeCache = _out = tuple(_out)
            return _out

    def __eq__(self, other):
        return self.getTypes() == other.getTypes()

class Text(BaseType):
    """Plain textual content."""

    isText = lambda s: True

class Raw(BaseType):
    """Raw regexp."""

    isRaw = lambda s: True

class Group(BaseType):
    """Grouping regexp."""

    isGroup = lambda s: True

class HiddenGroup(Group):

    isHiddenGroup = lambda s: True

class IndexedGroup(Group):

    isIndexedGroup = lambda s: True

class NamedGroup(Group):

    isNamedGroup = lambda s: True

# vim: set sts=4 sw=4
