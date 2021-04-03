#==============================================================================
# Massless particle in Minkowski space class
#------------------------------------------------------------------------------
#
#    real position is given in meters for x,z,y and nanosecenods for t as real values
#    grid position means position in numpy-like 4D array as integers 0..ix, 0..iy, 0..iz, 0..it
#
#    phi means argument (omega*t - k*x) as real value in radians
#    phs means phi mod 2*PI in radians
#
#------------------------------------------------------------------------------
from siqo_lib   import journal
from partCommon import PartCommon


from math     import sqrt, exp


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

#==============================================================================
# package's tools
#------------------------------------------------------------------------------

_MR_E           = 0.510998950002e6     # rest mass of electron in [eV/c2]

#==============================================================================
# class PartMassLess
#------------------------------------------------------------------------------
class PartMassLess(PartCommon):

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name, pos, eV):
        "Call constructor of PartMassLess and initialise it"

        journal.I( 'PartMassLess constructor for {}...'.format(name), 10 )
        
        super().__init__(name, pos, eV)
        self.type = 'MassLess'
        
        journal.O( 'PartMassLess {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        journal.M( 'PartMassLess {} ALL cleared'.format(self.name), 10)
        
    #==========================================================================
    # Tools for particle's selecting & editing
    #--------------------------------------------------------------------------

    #==========================================================================
    # Tools for Space 
    #--------------------------------------------------------------------------
    def getPhi(self, dPos):
        "Return angle Phi for particle and given interval in Minkowski space"
        
        rdt = dPos['dt'] - dPos['dr'] / _C
        
        return self.getOmega() * rdt

    #==========================================================================
    # Tools for data extraction & persistency
    #--------------------------------------------------------------------------
    def getJson(self):
        "Create and return Json record for particle"
        
        json = super().getJson()
        
        journal.M( 'PartMassLess {} getJson created'.format(self.name), 10)
        
        return json
        
    #--------------------------------------------------------------------------
    def print(self):
        "Return list of printable strings with particle's properties"
        
        toret = super().print()
        
        return toret
        
#------------------------------------------------------------------------------
print('PartMassLess class ver 0.11')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
