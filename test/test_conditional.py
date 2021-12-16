import o_re


def test_simple_cond():
    _brack1 = o_re.Text("(").asGroup()
    _brack2 = o_re.Text(")").asGroup()
    _sp = o_re.Space.times.any()
    _middleText = (o_re.Raw(r"\w+") + _sp).times.many().asGroup("text")
    _reg = \
        o_re.Sol + _sp + _brack1.times.maybe() + _sp + \
        _middleText + \
        _sp + o_re.If(_brack1, _brack2) + _sp + o_re.Eol
    _re = _reg.getCompiled()
    assert _re.match("  just some random text  ")
    assert _re.match("( just some random text )")
    assert not _re.match("( just some random text ")
    assert not _re.match("just some random text )")


def test_else_cond():
    _brack1 = o_re.Text("(").asGroup()
    _brack2 = o_re.Text(")").asGroup()
    _middleText = (o_re.Raw(r"\w+") + o_re.Space.times.any()).times.many().asGroup("text")
    _reg = o_re.tools.force_full_line(o_re.tools.space_sep((
            _brack1.times.maybe(),
            _middleText,
            o_re.If(_brack1, _brack2, "NO BRACKET")
        )),
        strict=False
    )
    _re = _reg.getCompiled()
    assert _re.match("  just some random text NO BRACKET ")
    assert _re.match("( just some random text )")
    assert not _re.match("( just some random text ")
    assert not _re.match("just some random text )")
