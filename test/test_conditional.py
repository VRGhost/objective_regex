import o_re


def test_simple_cond():
    _brack1 = o_re.Text("(").as_group()
    _brack2 = o_re.Text(")").as_group()
    _sp = o_re.Space.times.any()
    _middle_text = (o_re.Raw(r"\w+") + _sp).times.many().as_group("text")
    _reg = \
        o_re.Sol + _sp + _brack1.times.maybe() + _sp + \
        _middle_text + \
        _sp + o_re.If(_brack1, _brack2) + _sp + o_re.Eol
    _re = _reg.get_compiled()
    assert _re.match("  just some random text  ")
    assert _re.match("( just some random text )")
    assert not _re.match("( just some random text ")
    assert not _re.match("just some random text )")


def test_else_cond():
    _brack1 = o_re.Text("(").as_group()
    _brack2 = o_re.Text(")").as_group()
    _middle_text = (o_re.Raw(r"\w+") + o_re.Space.times.any()).times.many().as_group("text")
    _reg = o_re.tools.force_full_line(o_re.tools.space_sep((
            _brack1.times.maybe(),
            _middle_text,
            o_re.If(_brack1, _brack2, "NO BRACKET")
        )),
        strict=False
    )
    _re = _reg.get_compiled()
    assert _re.match("  just some random text NO BRACKET ")
    assert _re.match("( just some random text )")
    assert not _re.match("( just some random text ")
    assert not _re.match("just some random text )")
