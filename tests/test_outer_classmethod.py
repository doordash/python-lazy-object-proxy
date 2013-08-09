from __future__ import print_function

import unittest
import inspect
import imp

import wrapt

from wrapt import six

DECORATORS_CODE = """
import wrapt

@wrapt.decorator
def passthru_decorator(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)
"""

decorators = imp.new_module('decorators')
six.exec_(DECORATORS_CODE, decorators.__dict__, decorators.__dict__)

class Class(object):
    @classmethod
    def function(self, arg):
        '''documentation'''
        return arg

Original = Class

class Class(object):
    @classmethod
    @decorators.passthru_decorator
    def function(self, arg):
        '''documentation'''
        return arg

class TestNamingOuterClassMethod(unittest.TestCase):

    def test_class_object_name(self):
        # Test preservation of instance method __name__ attribute.

        self.assertEqual(Class.function.__name__,
                Original.function.__name__)

    def test_instance_object_name(self):
        # Test preservation of instance method __name__ attribute.

        self.assertEqual(Class().function.__name__,
                Original().function.__name__)

    def test_class_object_qualname(self):
        # Test preservation of instance method __qualname__ attribute.

        try:
            __qualname__ = Original.original.__qualname__
        except AttributeError:
            pass
        else:
            self.assertEqual(Class.function.__qualname__, __qualname__)

    def test_instance_object_qualname(self):
        # Test preservation of instance method __qualname__ attribute.

        try:
            __qualname__ = Original().original.__qualname__
        except AttributeError:
            pass
        else:
            self.assertEqual(Class().function.__qualname__, __qualname__)

    def test_class_module_name(self):
       # Test preservation of instance method __module__ attribute.

        self.assertEqual(Class.function.__module__,
                Original.function.__module__)

    def test_instance_module_name(self):
       # Test preservation of instance method __module__ attribute.

        self.assertEqual(Class().function.__module__,
                Original().function.__module__)

    def test_class_doc_string(self):
        # Test preservation of instance method __doc__ attribute.

        self.assertEqual(Class.function.__doc__,
                Original.function.__doc__)

    def test_instance_doc_string(self):
        # Test preservation of instance method __doc__ attribute.

        self.assertEqual(Class().function.__doc__,
                Original().function.__doc__)

    def test_class_argspec(self):
        # Test preservation of instance method argument specification.

        original_argspec = inspect.getargspec(Original.function)
        function_argspec = inspect.getargspec(Class.function)
        self.assertEqual(original_argspec, function_argspec)

    def test_instance_argspec(self):
        # Test preservation of instance method argument specification.

        original_argspec = inspect.getargspec(Original().function)
        function_argspec = inspect.getargspec(Class().function)
        self.assertEqual(original_argspec, function_argspec)

    def test_class_isinstance(self):
        # Test preservation of isinstance() checks.

        self.assertTrue(isinstance(Class.function,
                type(Original.function)))

    def test_instance_isinstance(self):
        # Test preservation of isinstance() checks.

        self.assertTrue(isinstance(Class().function,
                type(Original().function)))

class TestCallingOuterClassMethod(unittest.TestCase):

    def test_class_call_function(self):
        # Test calling classmethod. The instance and class passed to the
        # wrapper will both be None because our decorator is surrounded
        # by the classmethod decorator. The classmethod decorator
        # doesn't bind the method and treats it like a normal function,
        # explicitly passing the class as the first argument with the
        # actual arguments following that.

        _args = (1, 2)
        _kwargs = { 'one': 1, 'two': 2 }

        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            self.assertEqual(instance, None)
            self.assertEqual(args, (Class,)+_args)
            self.assertEqual(kwargs, _kwargs)
            return wrapped(*args, **kwargs)

        @_decorator
        def _function(*args, **kwargs):
            return args, kwargs

        class Class(object):
            @classmethod
            @_decorator
            def _function(cls, *args, **kwargs):
                return (args, kwargs)

        result = Class._function(*_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))

    def test_instance_call_function(self):
        # Test calling classmethod via class instance. The instance
        # and class passed to the wrapper will both be None because our
        # decorator is surrounded by the classmethod decorator. The
        # classmethod decorator doesn't bind the method and treats it
        # like a normal function, explicitly passing the class as the
        # first argument with the actual arguments following that.

        _args = (1, 2)
        _kwargs = { 'one': 1, 'two': 2 }

        @wrapt.decorator
        def _decorator(wrapped, instance, args, kwargs):
            self.assertEqual(instance, None)
            self.assertEqual(args, (Class,)+_args)
            self.assertEqual(kwargs, _kwargs)
            return wrapped(*args, **kwargs)

        @_decorator
        def _function(*args, **kwargs):
            return args, kwargs

        class Class(object):
            @classmethod
            @_decorator
            def _function(cls, *args, **kwargs):
                return (args, kwargs)

        result = Class()._function(*_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))