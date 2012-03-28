import ObjectiveRegex as mod

import base

class TestText(base.TestBase):


    def test_any(self):
        _reg = mod.ops.Any(["word1", "word2", "word3"])
        _re = _reg.getCompiled()
        self.assertTrue(_re.match("word1"))
        self.assertTrue(_re.match("word2"))
        self.assertTrue(_re.match("word3"))
        self.assertFalse(_re.match("word4"))

# vim: set sts=4 sw=4
