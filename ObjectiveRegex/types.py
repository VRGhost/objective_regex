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
