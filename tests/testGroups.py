import ObjectiveRegex as mod

import base

class TestGroups(base.TestBase):


    def test_numbered(self):
        _pat = mod.Raw("[a-d]+")
        _reg = _pat.asGroup() + mod.Raw(".*?") + _pat.asGroup()
        _m = _reg.getCompiled().search("poiopipouipipoioppippoipoi abcddcba qwqADDC abcdX")
        self.assertEqual(_m.group(1), "abcddcba")
        self.assertEqual(_m.group(2), "abcd")

    def test_named(self):
        _pat = mod.Raw("[a-d]+")
        _reg = _pat.asGroup("grp1") + mod.Raw(".*?") + _pat.asGroup("grp2")
        _m = _reg.getCompiled().search("poiopipouipipoioppippoipoi abcddcba qwqADDC abcdX")
        self.assertEqual(_m.group("grp1"), "abcddcba")
        self.assertEqual(_m.group("grp2"), "abcd")

    def test_numbered_reference(self):
        _pat = mod.Raw("ST\w+")
        _grp = _pat.asGroup()
        _reg = _grp + mod.Spaces + mod.Raw("\w+").asGroup() + mod.Spaces + _grp
        _m = _reg.getCompiled().match("ST123 ST424242 ST123")
        self.assertEqual(_m.group(1), "ST123")
        self.assertEqual(_m.group(2), "ST424242")

    def test_named_equality(self):
        _obj1 = mod.Raw("42").asGroup("name")
        _obj2 = mod.Raw("42").asGroup("name")
        self.assertEqual(_obj1, _obj2)
        _obj3 = mod.Raw("43").asGroup("name")
        self.assertNotEqual(_obj1, _obj3)
        self.assertNotEqual(_obj2, _obj3)


# vim: set sts=4 sw=4
