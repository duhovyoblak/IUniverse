#==============================================================================
# Massless particle in Minkowski space class
#------------------------------------------------------------------------------
#
#    real position is given in meters for x,z,y and nanosecenods for t as real values
#    grid position means position in numpy-like 4D array as integers 0..ix, 0..iy, 0..iz, 0..it
#
#    phi means argument (omega*t - k*x) as real value in radians
#
#------------------------------------------------------------------------------
from siqo_lib      import journal
from iuniverse_lib import _C
from partCommon    import PartCommon

from math          import sqrt, exp


#==============================================================================
# package's constants
#------------------------------------------------------------------------------


#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# class PartMassLess
#------------------------------------------------------------------------------
class PartMassLess(PartCommon):

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name, pos, eV=1):
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
