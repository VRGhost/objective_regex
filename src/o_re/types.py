"""Class for regex objects to be able to declare regex type"""
import enum


class RegexType(enum.Flag):

    Unknown = enum.auto()
    Text = enum.auto()

    _RawT = enum.auto()
    Raw = Text | _RawT

    Group = enum.auto()
    _HiddenG = enum.auto()
    HiddenGroup = Group | _HiddenG
    _IndexedG = enum.auto()
    IndexedGroup = Group | _IndexedG
    _NamedG = enum.auto()
    NamedGroup = Group | _NamedG

    def implemented_by(self, other: enum.Flag):
        return (self & other) == self
