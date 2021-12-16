import o_re

def test_numbered():
    _pat = o_re.Raw("[a-d]+")
    _reg = _pat.asGroup() + o_re.Raw(".*?") + _pat.asGroup()
    _m = _reg.getCompiled().search("poiopipouipipoioppippoipoi abcddcba qwqADDC abcdX")
    assert _m.group(1) == "abcddcba"
    assert _m.group(2) == "abcd"

def test_named():
    _pat = o_re.Raw("[a-d]+")
    _reg = _pat.asGroup("grp1") + o_re.Raw(".*?") + _pat.asGroup("grp2")
    _m = _reg.getCompiled().search("poiopipouipipoioppippoipoi abcddcba qwqADDC abcdX")
    assert _m.group("grp1") == "abcddcba"
    assert _m.group("grp2") == "abcd"

def test_numbered_reference():
    _pat = o_re.Raw(r"ST\w+")
    _grp = _pat.asGroup()
    _reg = _grp + o_re.Spaces + o_re.Raw(r"\w+").asGroup() + o_re.Spaces + _grp
    _m = _reg.getCompiled().match("ST123 ST424242 ST123")
    assert _m.group(1) == "ST123"
    assert _m.group(2) == "ST424242"

def test_named_equality():
    _obj1 = o_re.Raw("42").asGroup("name")
    _obj2 = o_re.Raw("42").asGroup("name")
    assert _obj1 == _obj2
    _obj3 = o_re.Raw("43").asGroup("name")
    assert _obj1 != _obj3
    assert _obj2 != _obj3


# vim: set sts=4 sw=4