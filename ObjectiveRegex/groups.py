import itertools


from . import base

class GroupBase(base.RegexBase):
    """Base class for all group objects."""

    isGroup = True
    wrap = "[[[I AM GROUP {!r}]]]"

    def __init__(self, children):
        super(GroupBase, self).__init__()
        self.children = list(children)

    def _getRegex(self, ctx):
        return self.wrap.format(super(GroupBase, self)._getRegex(ctx))

class HiddenGroup(GroupBase):
    """Hidden group that does not influence resulting matcher."""

    isHiddenGroup = True
    wrap = "(?:{})"

    # custom overrides for output regex simplification

    _asHiddenGroup = lambda self: self

    def append(self, other):
        if getattr(other, "isHiddenGroup", False):
            _obj = other
        else:
            _obj = HiddenGroup((other, ))
        self.children.append(_obj)
        return self

class Group(GroupBase):
    """Index-accessed group"""

    isIndexedGroup = True

    wrap = "({})"

    def _getRegex(self, ctx):
        if ctx.haveVisited(self):
            for (_id, _grp) in enumerate(itertools.ifilter(lambda el: getattr(el, "isIndexedGroup", False), ctx.visited)):
                if _grp is self:
                    _foundId = _id + 1
                    break
            else:
                raise RuntimeError("Expected for this group to have been found")

            return "\\{}".format(_foundId)
        else:
            return super(Group, self)._getRegex(ctx)

class NamedGroup(GroupBase):
    """Group accessed by name."""

    isNamedGroup = True
    wrap = "(?P<{name}>{regex})"

    def __init__(self, children, name):
        super(NamedGroup, self).__init__(children)
        self.name = name

    def _getRegex(self, ctx):
        if ctx.haveVisited(self):
            return "(?P={})".format(self.name)
        else:
            return self.wrap.format(
                name=self.name,
                regex=super(GroupBase, self)._getRegex(ctx),
            )

# vim: set sts=4 sw=4 et :
