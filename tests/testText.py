import ObjectiveRegex as mod

import base

class TestText(base.TestBase):


    def test_raw(self):
        _pat = "(\d+)"
        _reg = mod.Raw(_pat)
        self.assertEqual(_pat, _reg.getRegex())
        _text = "kasdhfjkasdhfjkasdfh 4242 laskfjlsdfkjglsdkg"
        _m = _reg.getCompiled().search(_text)
        self.assertEqual(_m.groups(), ("4242", ))

    def test_text(self):
        _pat = "^.*$"
        _reg = mod.Text(_pat)
        self.assertNotEqual(_pat, _reg.getRegex())
        _re = _reg.getCompiled()
        self.assertTrue(_re.match("^.*$"))
        self.assertFalse(_re.match("4242"))

    def test_rconcat(self):
        _reg = mod.Text("hello ") + "world!"
        _re = _reg.getCompiled()
        self.assertTrue(_re.match("hello world!"))

    def test_lconcat(self):
        _reg = "hello " + mod.Text("world!")
        _re = _reg.getCompiled()
        self.assertTrue(_re.match("hello world!"))

# vim: set sts=4 sw=4
