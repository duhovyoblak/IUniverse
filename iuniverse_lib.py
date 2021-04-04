#==============================================================================
# IUniverse project common library
#------------------------------------------------------------------------------
#
#    real position is given in meters for x,z,y and nanosecenods for t as real values
#    grid position means position in numpy-like 4D array as integers 0..ix, 0..iy, 0..iz, 0..it
#
#    phi means argument (omega*t - k*x) as real value in radians
#    phs means phi mod 2*PI in radians
#
#------------------------------------------------------------------------------
from siqo_lib import journal
from math     import sqrt

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

_ERR            = '_ERROR_'

_E              = 2.718281828459045    # Euler number
_PI             = 3.141592653589793    # Pi number
_2PI            = 2 * _PI              # 2 * Pi
_SQRT_2PI       = sqrt(_2PI)
_REV_SQRT_2PI   = 1 / _SQRT_2PI

_H              = 6.62607015e-34       # Planck quantum in [Joule*second]
_H_RED          = _H / _2PI            # Reduced Planck quantum
_C              = 299792458            # speed of light in [meter/second]
_C2             = _C * _C              # speed of light square
_EV_J           = 1.602176634e-19      # energy of 1 eV in [Joule]
_EV_KG          = 1.782662e-36         # mass   of 1 eV/c2 in [kg]


_MR_E           = 0.510998950002e6     # rest mass of electron in [eV/c2]

        
#------------------------------------------------------------------------------
print('IUniverse library ver 0.10')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
