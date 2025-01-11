#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
from weakref import WeakSet, WeakKeyDictionary


__all__ = ["Signal"]


class Signal(object):
    def __init__(self):
        self._functions = WeakSet()
        self._methods = WeakKeyDictionary()
        self._activated = True

    def __call__(self, *args, **kargs):
        # call connected functions only if activated
        if self._activated:
            # Call handler functions
            for func in self._functions:
                func(*args, **kargs)

            # Call handler methods
            for obj, funcs in self._methods.items():
                for func in funcs:
                    func(obj, *args, **kargs)

    def connect(self, slot):
        if inspect.ismethod(slot):
            if slot.__self__ not in self._methods:
                self._methods[slot.__self__] = set()

            self._methods[slot.__self__].add(slot.__func__)

        else:
            self._functions.add(slot)

    def disconnect(self, slot):
        if inspect.ismethod(slot):
            if slot.__self__ in self._methods:
                self._methods[slot.__self__].remove(slot.__func__)
        else:
            if slot in self._functions:
                self._functions.remove(slot)

    def clear(self):
        self._functions.clear()
        self._methods.clear()

    def activate(self):
        """
        Activate the signal to emit.
        """
        self._activated = True

    def deactivate(self):
        """
        Deactivate the signal to emit.
        """
        self._activated = False

    def show(self):
        """
        Show all connected slots to the signal.
        """
        return "Methods: {0}\nFunctions: {1}".format(
            dict(self._methods),
            set(self._functions),
        )
