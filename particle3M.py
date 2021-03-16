#==============================================================================
# Common particle in Minkowski space class
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


from math     import sqrt, exp


#==============================================================================
# package's constants
#------------------------------------------------------------------------------

_ERR            = '_ERROR_'

_PI             = 3.141592653589793    # Pi number
_2PI            = 6.283185307179586
_SQRT_2PI       = 2.5066282746310002
_REV_SQRT_2PI   = 0.3989422804014327

_E              = 2.718281828459045    # Euler number
_H              = 6.62607015e-25       # Planck quantum in [Joule*nanosecond]
_H_RED          = _H / _2PI            # Reduced Planck quantum
_C              = 0.299792458          # speed of light in [meter/nanosecond]
_C2             = _C * _C              # speed of light square
_EV             = 1.602176634e-19      # energy of 1 eV in [Joule]

#==============================================================================
# package's tools
#------------------------------------------------------------------------------

_M_E            = 0.510998950002e6     # rest mass of electron in [eV]

#==============================================================================
# class Particle3M
#------------------------------------------------------------------------------
class Particle3M:

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name, f, k):
        "Call constructor of Particle3M and initialise its frequency and wave vector"

        journal.I( 'Particle3M constructor for {}...'.format(name), 10 )
        
        self.name = name   # unique name for particle in Your project
        self.f    = f      # frequency in [GHz]
        self.k    = k      # wavenumber {'kx', 'ky', 'kz'} in [meter]
        
        self.pos  = {'x':0, 'y':0, 'z':0, 't':0}     # Default position

        journal.O( 'Particle3M {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        journal.M( 'Particle3M {} ALL cleared'.format(self.name), 10)
        
    #==========================================================================
    # Tools for particle's selecting & editing
    #--------------------------------------------------------------------------
    def getName(self):
        "Return particles's name"
        
        return self.name

    #--------------------------------------------------------------------------
    def getPos(self):
        "Return particles's real position"
        
        return self.pos

    #--------------------------------------------------------------------------
    def getEnergyT(self):
        "Return total energy of particle in [Joule]"
        
        return _H * self.f
    
    #--------------------------------------------------------------------------
    def getEnergyR(self):
        "Return rest energy of particle in [Joule]"
        
        return 0
    
    #--------------------------------------------------------------------------
    def getMassT(self):
        "Return total mass of particle in [eV]"
        
        return self.
    
    #--------------------------------------------------------------------------
    def getMassR(self):
        "Return rest mass of particle in [eV]"
        
        return 
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #==========================================================================
    # Tools for Space 
    #--------------------------------------------------------------------------
    def toSpace(self, space, pos='nil'):
        "Write particle to Minkowski space"
        
        journal.I( 'Particle3M {} toSpace...'.format(self.name), 10)
        
        if pos!='nil': self.pos = pos
        
        for cell in space.act.values():
            
            pos = cell['pos']
            val = cell['val']
            
            val['phi'] = space.getDPos(self.pos, pos)
            

        
        journal.O( 'Particle3M {} toSpace done'.format(self.name), 10)

    #==========================================================================
    # Tools for data extraction & persistency
    #--------------------------------------------------------------------------
    def getJson(self):
        "Create and return Json record"
        
        json = {'name':self.name, 'pos':self.pos}
        
        journal.M( 'Particle3M {} getJson created'.format(self.name), 10)
        
        return json
        
#------------------------------------------------------------------------------
print('Particle class ver 0.10')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
