"""Regex construction context that raises an exception if more than one regex context is initialized simultaneously."""

import weakref
import gc
import unittest

class SingletonContextHandler(object):

    installed = False
    _existingContext = None

    def __init__(self):
        super(SingletonContextHandler, self).__init__()
        from ObjectiveRegex import construction
        self.target = construction
        self.origCls = construction.Context

    def install(self):
        if self.installed:
            raise RuntimeError("Already installed.")

        self.target.Context = self
        self.installed = True

    def __call__(self, *args, **kwargs):
        """Called when the code wants to create new 'Context' instance"""
        if self._contextAlreadyExists():
            raise RuntimeError("Context already exists")

        _obj = self.origCls(*args, **kwargs)
        self._existingContext = weakref.ref(_obj)
        return _obj

    def _contextAlreadyExists(self):
        # Force gc to collect any unreferenced contexts
        gc.collect()
        _ref = self._existingContext
        return _ref and _ref()

    def remove(self):
        if self._contextAlreadyExists():
            raise RuntimeError("No contexts are expected to be existing")
        self.target.Context = self.origCls
        self.installed = False


_HANDLER = SingletonContextHandler()

class TestBase(unittest.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        _HANDLER.install()

    def tearDown(self):
        super(TestBase, self).tearDown()
        _HANDLER.remove()

# vim: set sts=4 sw=4
