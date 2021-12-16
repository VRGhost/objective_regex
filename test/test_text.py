import o_re


def test_raw():
    _pat = r"(\d+)"
    _reg = o_re.Raw(_pat)
    assert _pat == _reg.get_regex()
    _text = "kasdhfjkasdhfjkasdfh 4242 laskfjlsdfkjglsdkg"
    _m = _reg.get_compiled().search(_text)
    assert _m.groups() == ("4242", )


def test_text():
    _pat = "^.*$"
    _reg = o_re.Text(_pat)
    assert _pat != _reg.get_regex()
    _re = _reg.get_compiled()
    assert _re.match("^.*$")
    assert not _re.match("4242")


def test_rconcat():
    _reg = o_re.Text("hello ") + "world!"
    _re = _reg.get_compiled()
    assert _re.match("hello world!")


def test_lconcat():
    _reg = "hello " + o_re.Text("world!")
    _re = _reg.get_compiled()
    assert _re.match("hello world!")
