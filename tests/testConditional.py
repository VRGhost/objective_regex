import ObjectiveRegex as mod

import base

class TestText(base.TestBase):


    def test_simple_cond(self):
        _brack1 = mod.Text("(").asGroup()
        _brack2 = mod.Text(")").asGroup()
        _sp = mod.Space.times.any()
        _middleText = (mod.Raw("\w+") + _sp).times.many().asGroup("text")
        _reg = mod.Sol + _sp + _brack1.times.maybe() + _sp + \
                _middleText + \
                _sp + mod.If(_brack1, _brack2) + _sp + mod.Eol
        _re = _reg.getCompiled()
        self.assertTrue(_re.match("  just some random text  "))
        self.assertTrue(_re.match("( just some random text )"))
        self.assertFalse(_re.match("( just some random text "))
        self.assertFalse(_re.match("just some random text )"))

    def test_else_cond(self):
        _brack1 = mod.Text("(").asGroup()
        _brack2 = mod.Text(")").asGroup()
        _middleText = (mod.Raw("\w+") + mod.Space.times.any()).times.many().asGroup("text")
        _reg = mod.tools.force_full_line(mod.tools.space_sep((
                _brack1.times.maybe(),
                _middleText,
                mod.If(_brack1, _brack2, "NO BRACKET")
            )),
            strict=False
        )
        _re = _reg.getCompiled()
        self.assertTrue(_re.match("  just some random text NO BRACKET "))
        self.assertTrue(_re.match("( just some random text )"))
        self.assertFalse(_re.match("( just some random text "))
        self.assertFalse(_re.match("just some random text )"))

# vim: set sts=4 sw=4
