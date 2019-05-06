"""Define some useful definitions for emopt.
"""

from builtins import object
__author__ = "Andrew Michaels"
__license__ = "GPL License, Version 3.0"
__version__ = "0.4"
__maintainer__ = "Andrew Michaels"
__status__ = "development"

class FieldComponent(object):
    Ex = 'Ex'
    Ey = 'Ey'
    Ez = 'Ez'
    Hx = 'Hx'
    Hy = 'Hy'
    Hz = 'Hz'

class SourceComponent(object):
    Jx = 'Jx'
    Jy = 'Jy'
    Jz = 'Jz'
    Mx = 'Mx'
    My = 'My'
    Mz = 'Mz'
