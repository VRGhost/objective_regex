import o_re

def test_any():
    _reg = o_re.ops.Any(["word1", "word2", "word3"])
    _re = _reg.getCompiled()
    assert _re.match("word1")
    assert _re.match("word2")
    assert _re.match("word3")
    assert not _re.match("word4")

# vim: set sts=4 sw=4
