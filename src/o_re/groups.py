from . import base, text, types


class GroupBase(base.RegexBase):
    """Base class for all group objects."""

    type = types.RegexType.Group

    wrap = "[[[I AM GROUP {!r}]]]"

    def __init__(self, children):
        super(GroupBase, self).__init__()
        self.children = list(children)

    def _getRegex(self, ctx):
        return self.wrap.format(super(GroupBase, self)._getRegex(ctx))

    def asReference(self, ctx):
        """Return given group as reference (pointer)"""
        raise NotImplementedError

    def getName(self, ctx):
        """Return name of given group in given context."""
        raise NotImplementedError


class HiddenGroup(GroupBase):
    """Hidden group that does not influence resulting matcher."""

    type = types.RegexType.HiddenGroup
    wrap = "(?:{})"

    # custom overrides for output regex simplification


class Group(GroupBase):
    """Index-accessed group"""

    type = types.RegexType.IndexedGroup
    wrap = "({})"

    def _getRegex(self, ctx):
        if tuple(ctx.getVisited(lambda el: el is self)):
            return self.asReference(ctx)._getRegex(ctx)
        else:
            return super(Group, self)._getRegex(ctx)

    def getName(self, ctx):
        for (_id, _grp) in enumerate(ctx.getVisited(
            lambda el: types.RegexType.IndexedGroup.implemented_by(el.type)
        )):
            if _grp is self:
                _foundId = _id + 1
                break
        else:
            if ctx.strict:
                raise RuntimeError("Unable to find this group in current context.")
            else:
                _foundId = "!? Unable to determine ID ?!"

        return _foundId

    def asReference(self, ctx):
        return text.Raw("\\{}".format(self.getName(ctx)))


class NamedGroup(GroupBase):
    """Group accessed by name."""

    type = types.RegexType.NamedGroup
    wrap = "(?P<{name}>{regex})"
    name = None

    def __init__(self, children, name):
        super(NamedGroup, self).__init__(children)
        self.name = name

    def _getRegex(self, ctx):
        _visited = tuple(ctx.getVisited(
            lambda el: types.RegexType.NamedGroup.implemented_by(el.type) and el.name == self.name
        ))
        if _visited:
            return self.asReference(ctx)._getRegex(ctx)
        else:
            return self.wrap.format(
                name=self.name,
                regex=super(GroupBase, self)._getRegex(ctx),
            )

    def getName(self, ctx):
        return self.name

    def asReference(self, ctx):
        return text.Raw("(?P={})".format(self.getName(ctx)))

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name and self.children == other.children
