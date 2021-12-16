from . import base, text, types


class GroupBase(base.RegexBase):
    """Base class for all group objects."""

    type = types.RegexType.Group

    wrap = "[[[I AM GROUP {!r}]]]"

    def __init__(self, children):
        super(GroupBase, self).__init__()
        self.children = list(children)

    def _get_regex(self, ctx):
        return self.wrap.format(super(GroupBase, self)._get_regex(ctx))

    def as_reference(self, ctx):
        """Return given group as reference (pointer)"""
        raise NotImplementedError

    def get_name(self, ctx):
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

    def _get_regex(self, ctx):
        if tuple(ctx.get_visited(lambda el: el is self)):
            return self.as_reference(ctx)._get_regex(ctx)
        else:
            return super(Group, self)._get_regex(ctx)

    def get_name(self, ctx):
        for (_id, _grp) in enumerate(ctx.get_visited(
            lambda el: types.RegexType.IndexedGroup.implemented_by(el.type)
        )):
            if _grp is self:
                _found_id = _id + 1
                break
        else:
            if ctx.strict:
                raise RuntimeError("Unable to find this group in current context.")
            else:
                _found_id = "!? Unable to determine ID ?!"

        return _found_id

    def as_reference(self, ctx):
        return text.Raw("\\{}".format(self.get_name(ctx)))


class NamedGroup(GroupBase):
    """Group accessed by name."""

    type = types.RegexType.NamedGroup
    wrap = "(?P<{name}>{regex})"
    name = None

    def __init__(self, children, name):
        super(NamedGroup, self).__init__(children)
        self.name = name

    def _get_regex(self, ctx):
        _visited = tuple(ctx.get_visited(
            lambda el: types.RegexType.NamedGroup.implemented_by(el.type) and el.name == self.name
        ))
        if _visited:
            return self.as_reference(ctx)._get_regex(ctx)
        else:
            return self.wrap.format(
                name=self.name,
                regex=super(GroupBase, self)._get_regex(ctx),
            )

    def get_name(self, ctx):
        return self.name

    def as_reference(self, ctx):
        return text.Raw("(?P={})".format(self.get_name(ctx)))

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name and self.children == other.children
