'''Non-rebinding properties

Helps define a constant in Python
From Section 6.3: Defining Constants
Python Cookbook (2 Ed) by Alex Martelli et al.

Usage:
import const
const.magic = 23 # First binding is fine
const.magic = 88 # Second binding raises const.ConstError
del const.magic # deleting is not fine
'''

import sys
class _const:
    class ConstError(TypeError):
        '''Error thrown on any change of property of the class `_const`.
        '''
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const(%s)" %name)
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError("Can't unbind const(%s)" %name)
        raise NameError(name)

sys.modules[__name__] = _const()
