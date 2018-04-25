"""Miscellanious functions useful for simulation and optimization.
"""

import numpy as np
from scipy import interpolate
import os

from petsc4py import PETSc
#import decorator # so that sphinx will document decorated functions :S
import warnings, inspect

__author__ = "Andrew Michaels"
__license__ = "GPL License, Version 3.0"
__version__ = "0.2"
__maintainer__ = "Andrew Michaels"
__status__ = "development"

# functions and variables useful for MPI stuff
COMM = PETSc.COMM_WORLD.tompi4py()
RANK = PETSc.COMM_WORLD.getRank()
NOT_PARALLEL = (RANK == 0)

def run_on_master(func):
    """Prevent a decorated function from running on any node but the master
    node
    """

    def wrapper(*args, **kwargs):
        if(NOT_PARALLEL):
            return func(*args, **kwargs)
        else:
            return

    return wrapper

def n_silicon(wavelength):
    """Load silicon refractive index vs wavlength and interpolate at desired wavelength.
    A piecewise cubic fit is used for the interpolation.

    Parameters
    ----------
    wavelength : float
        The wavlenegth in [um] between 1.2 um and 14 um

    Returns
    -------
        Refractive index of silicon at desired wavelength.
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = ''.join([dir_path, '/data/silicon.csv'])

    data_si = np.loadtxt(data_path, delimiter=',', skiprows=1)
    wlen_si = data_si[:,0]
    n_si = data_si[:,1]
    n_interp = interpolate.interp1d(wlen_si, n_si, kind='cubic')

    return n_interp(wavelength)



def info_message(message):
    """Print a formatted, easily-distinguishable message.

    Parameters
    ----------
    message : str
        The message to print.
    """
    print(u'\u001b[46;1m[INFO]\u001b[0m %s' % (message))

class EMOptWarning(RuntimeWarning):
    pass

@run_on_master
def _warning_message(message, category=UserWarning, filename='', lineno=-1):
    # Override python's warning message by adding a colored [WARNING] flag in
    # front to make it more noticeable.
    if(type(category) == EMOptWarning):
        print(u'\u001b[43;1m[WARNING]\u001b[0m %s' % (message))
    else:
        print(u'\u001b[43;1m[WARNING]\u001b[0m in %s at line %d: %s' % \
              (filename, lineno, message))
warnings.showwarning = _warning_message


def warning_message(message, module):
    # Produce a warning message to warn the user that a problem has occurred.
    # This is primarily intended for internal use within emopt
    warnings.warn('in %s: %s' % (module, message), category=EMOptWarning)

def error_message(message):
    """Print a formatted, easily-distinguishable error message.

    In general, exceptions are probably preferable, but if you ever want to
    throw a non-disrupting error whose format is consistent with info_message
    and warning_message, use this!

    Parameters
    ----------
    message : str
        The message to print.
    """
    print(u'\u001b[41;1m[ERROR]\u001b[0m %s' % (message))


class DomainCoordinates(object):
    """Define a domain coordinate.

    A DomainCoordinate is a class which manages accessing data on a rectangular
    grid. It stores both the indexed positions and real-space coordinates of a
    desired line, plane, or volume.

    Attributes
    ----------
    x : numpy.ndarray
        The real-space x coordinates of the domain
    y : numpy.ndarray
        The real-space y coordinates of the domain
    z : numpy.ndarray
        The real-space z coordinates of the domain
    i : slice
        The slice along the z direction
    j : slice
        The slice along the y direction
    k : numpy.ndarray
        The slice along the x direction
    Nx : int
        The number of x indices in the domain
    Ny : int
        The number of y indices in the domain
    Nz : int
        The number of z indices in the domain
    xspan : float
        The physical size of the domain in the x direction
    yspan : float
        The physical size of the domain in the y direction
    zspan : float
        The physical size of the domain in the z direction
    dx : float
        The grid spacing in x direction
    dy : float
        The grid spacing in y direction
    dz : float
        The grid spacing in z direction
    """

    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax, dx, dy, dz):
        i1 = int(zmin/dz)
        i2 = int(zmax/dz)+1
        ilist = np.arange(i1, i2, 1, dtype=np.int)
        self._z = dz * ilist.astype(np.double)
        self._i = slice(i1, i2)

        j1 = int(ymin/dy)
        j2 = int(ymax/dy)+1
        jlist = np.arange(j1, j2, 1, dtype=np.int)
        self._y = dy * jlist.astype(np.double)
        self._j = slice(j1, j2)

        k1 = int(xmin/dx)
        k2 = int(xmax/dx)+1
        klist = np.arange(k1, k2, 1, dtype=np.int)
        self._x = dx * klist.astype(np.double)
        self._k = slice(k1, k2)

        self._Nx = k2 - k1
        self._Ny = j2 - j1
        self._Nz = i2 - i1

        self._xspan = dx * (self._Nx-1)
        self._yspan = dy * (self._Ny-1)
        self._zspan = dz * (self._Nz-1)

        self._dx = dx
        self._dy = dy
        self._dz = dz


    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @x.setter
    def x(self, value):
        warning_message('x cannot be reassigned in this way.', 'emopt.misc')

    @y.setter
    def y(self, value):
        warning_message('y cannot be reassigned in this way.', 'emopt.misc')

    @z.setter
    def z(self, value):
        warning_message('z cannot be reassigned in this way.', 'emopt.misc')

    @property
    def i(self):
        return self._i

    @property
    def j(self):
        return self._j

    @property
    def k(self):
        return self._k

    @i.setter
    def i(self, value):
        warning_message('i cannot be reassigned in this way.', 'emopt.misc')

    @j.setter
    def j(self, value):
        warning_message('j cannot be reassigned in this way.', 'emopt.misc')

    @k.setter
    def k(self, value):
        warning_message('k cannot be reassigned in this way.', 'emopt.misc')

    @property
    def Nx(self):
        return self._Nx

    @property
    def Ny(self):
        return self._Ny

    @property
    def Nz(self):
        return self._Nz

    @Nx.setter
    def Nx(self, value):
        warning_message('Nx cannot be reassigned in this way.', 'emopt.misc')

    @Ny.setter
    def Ny(self, value):
        warning_message('Ny cannot be reassigned in this way.', 'emopt.misc')

    @Nz.setter
    def Nz(self, value):
        warning_message('Nz cannot be reassigned in this way.', 'emopt.misc')

    @property
    def xspan(self):
        return self._xspan

    @property
    def yspan(self):
        return self._xspan

    @property
    def zspan(self):
        return self._zspan

    @xspan.setter
    def xspan(self, value):
        warning_message('xspan cannot be reassigned in this way.', 'emopt.misc')

    @yspan.setter
    def yspan(self, value):
        warning_message('yspan cannot be reassigned in this way.', 'emopt.misc')

    @zspan.setter
    def zspan(self, value):
        warning_message('zspan cannot be reassigned in this way.', 'emopt.misc')

    @property
    def dx(self):
        return self._dx

    @property
    def dy(self):
        return self._dy

    @property
    def dz(self):
        return self._dz

    @dx.setter
    def dx(self, value):
        warning_message('dx cannot be reassigned in this way.', 'emopt.misc')

    @dy.setter
    def dy(self, value):
        warning_message('dy cannot be reassigned in this way.', 'emopt.misc')

    @dz.setter
    def dz(self, value):
        warning_message('dz cannot be reassigned in this way.', 'emopt.misc')

    def get_bounding_box(self):
        return [np.min(self._x), np.max(self._x), np.min(self._y),
                np.max(self._y), np.min(self._z), np.max(self._z),]


####################################################################################
# Define a MathDummy
####################################################################################

class MathDummy(np.ndarray):
    """Define a MathDummy.

    A MathDummy is an empty numpy.ndarray which devours all mathematical
    operations done by it or on it and just spits itself back out. This is
    used by emopt in order simplify its interface in the presence of MPI. For
    example, in many instances, you will need to calculate a quantity which
    need only be known on the master node, however the function performing the
    computation will be run on all nodes. Rather than having to worry about
    putting in if(NOT_PARALLEL) statements everywhere, we can just sneakily
    replace quantities involved in the calculation with MathDummies on all
    nodes but the master node.  You can then do any desired calculations
    without worying about what's going on in the other nodes.
    """
    def __new__(cls):
        obj = np.asarray([]).view(cls)
        return obj

    def __add__(self, other): return self
    def __sub__(self, other): return self
    def __mul__(self, other): return self
    def __matmul__(self, other): return self
    def __truediv__(self, other): return self
    def __floordiv__(self, other): return self
    def __mod__(self, other): return self
    def __divmod__(self, other): return self
    def __pow__(self, other, modulo=2): return self
    def __lshift__(self, other): return self
    def __rshift__(self, other): return self
    def __and__(self, other): return self
    def __xor__(self, other): return self
    def __or__(self, other): return self
    def __radd__(self, other): return self
    def __rsub__(self, other): return self
    def __rmul__(self, other): return self
    def __rmatmul__(self, other): return self
    def __rtruediv__(self, other): return self
    def __rfloordiv__(self, other): return self
    def __rmod__(self, other): return self
    def __rdivmod__(self, other): return self
    def __rpow__(self, other): return self
    def __rlshift__(self, other): return self
    def __rrshift__(self, other): return self
    def __rand__(self, other): return self
    def __rxor__(self, other): return self
    def __ror__(self, other): return self
    def __iadd__(self, other): return self
    def __isub__(self, other): return self
    def __imul__(self, other): return self
    def __imatmul__(self, other): return self
    def __itruediv__(self, other): return self
    def __ifloordiv__(self, other): return self
    def __imod__(self, other): return self
    def __ipow__(self, other, modulo=2): return self
    def __ilshift__(self, other): return self
    def __irshift__(self, other): return self
    def __iand__(self, other): return self
    def __ixor__(self, other): return self
    def __ior__(self, other): return self
    def __neg__(self): return self
    def __pos__(self): return self
    def __abs__(self): return self
    def __invert__(self): return self
    def __complex__(self): return self
    def __int__(self): return self
    def __float__(self): return self
    def __round__(self, n): return self
    def __index__(self): return 0
    def __getitem__(self, key): return self
    def __setitem__(self, key, value): return self

def get_dark_cmaps():
    """Generate dark-themed colormaps for eye-friendly visualization.

    Returns
    -------
    tuple
        Two matplotlib colormaps. The first color map is for +/- image data
        while the second is intended for strictly positive valued images.
    """
    from matplotlib.colors import LinearSegmentedColormap
    field_cols=['#3d9aff', '#111111', '#ff3d63']
    field_cmap=LinearSegmentedColormap.from_list('field_cmap', field_cols)

    struct_cols=['#212730', '#bcccdb']
    struct_cmap=LinearSegmentedColormap.from_list('struct_cmap', struct_cols)

    return field_cmap, struct_cmap
