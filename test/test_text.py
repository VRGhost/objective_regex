import o_re

def test_raw():
    _pat = r"(\d+)"
    _reg = o_re.Raw(_pat)
    assert _pat == _reg.getRegex()
    _text = "kasdhfjkasdhfjkasdfh 4242 laskfjlsdfkjglsdkg"
    _m = _reg.getCompiled().search(_text)
    assert _m.groups() == ("4242", )

def test_text():
    _pat = "^.*$"
    _reg = o_re.Text(_pat)
    assert _pat != _reg.getRegex()
    _re = _reg.getCompiled()
    assert _re.match("^.*$")
    assert not _re.match("4242")

def test_rconcat():
    _reg = o_re.Text("hello ") + "world!"
    _re = _reg.getCompiled()
    assert _re.match("hello world!")

def test_lconcat():
    _reg = "hello " + o_re.Text("world!")
    _re = _reg.getCompiled()
    assert _re.match("hello world!")

# vim: set sts=4 sw=4
