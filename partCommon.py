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
# class PartCommon
#------------------------------------------------------------------------------
class PartCommon:

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name, pos, eV):
        "Call constructor of PartCommon and initialise it"

        journal.I( 'PartCommon constructor for {}...'.format(name), 10 )
        
        self.name     = name      # unique name for particle in Your project
        self.type     = 'common'  # type of particle, used in inherited classes
        self.pos      = pos       # position of probability density amplitude origin
        self.eV       = eV        # energy of article in [eV]

        journal.O( 'PartCommon {} created with {:e} eV'.format(self.name, self.eV), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        journal.M( 'PartCommon {} ALL cleared'.format(self.name), 10)
        
    #==========================================================================
    # Tools for particle's selecting & editing
    #--------------------------------------------------------------------------
    def getName(self):
        "Return particles's name"
        
        return self.name

    #--------------------------------------------------------------------------
    def getType(self):
        "Return particles's type"
        
        return self.type

    #--------------------------------------------------------------------------
    def setEV(self, eV):
        "Set total energy in [eV]"
        
        self.eV = eV

    #--------------------------------------------------------------------------
    def setLambda(self, lam):
        "Set total energy in [eV] for given lambda in [m], E = h * c / lambda * coeff"
        
        self.eV = _H * _C / lam / _EV_J

    #==========================================================================
    # Physical properties of common particle
    #--------------------------------------------------------------------------
    def getEV(self):
        "Return total energy of particle in [eV]"
        
        return self.eV
    
    #--------------------------------------------------------------------------
    def getEJ(self):
        "Return total energy of particle in [J], E = coeff * eV"
        
        return _EV_J * self.eV
    
    #--------------------------------------------------------------------------
    def getMass(self):
        "Return total mass of particle in [kg], m = E/c2"
        
        return self.getEJ() / _C2
    
    #--------------------------------------------------------------------------
    def getAbsMoment(self):
        "Return absolute value of momentum, p = E/c in [kg*m/s]"
        
        return self.getEJ() / _C
        
    #==========================================================================
    # Physical properties in wave format
    #--------------------------------------------------------------------------
    def getFreq(self):
        "Return frequency in [Hz], f = E / h "
        
        return self.getEJ() / _H
        
    #--------------------------------------------------------------------------
    def getOmega(self):
        "Return frequency in [rad/s], omega = 2Pi * f"
        
        return _2PI * self.getFreq()
        
    #--------------------------------------------------------------------------
    def getLambda(self):
        "Return wavelength in [m], lambda = c/f"
        
        return _C / self.getFreq()
    
    #--------------------------------------------------------------------------
    def getWaveNum(self):
        "Return wave  number in [2Pi/m], k = 2Pi / lambda"
        
        return _2PI / self.getLambda()
    
    #--------------------------------------------------------------------------
    
    #==========================================================================
    # Tools for Space 
    #--------------------------------------------------------------------------
    def toSpace(self, space, pos='nil'):
        "Write particle to Minkowski space"
        
        journal.I( 'PartCommon {} toSpace...'.format(self.name), 10)
        
        if pos!='nil': self.pos = pos
        
        for cell in space.act.values():
            
            pos = cell['pos']
            val = cell['val']
            
            val['phi'] = space.getDPos(self.pos, pos)
            

        
        journal.O( 'PartCommon {} toSpace done'.format(self.name), 10)

    #==========================================================================
    # Tools for data extraction & persistency
    #--------------------------------------------------------------------------
    def getJson(self):
        "Create and return Json record for particle"
        
        json = {'name':self.name, 'type':self.type, 'eV':self.eV}
        
        journal.M( 'PartCommon {} getJson created'.format(self.name), 10)
        
        return json
        
    #--------------------------------------------------------------------------
    def print(self):
        "Print particle's properties"
        
        print( "Particle '{}' is of type '{}'".format(self.name, self.type) )
        print( "Position x={:e}, y={:e}, z={:e}, t={:e}".format(self.pos['x'], self.pos['y'], self.pos['z'], self.pos['t']))
        print( "-----------------------------------------------------------------------" )
        print( "Total Energy {:e} [eV]        total Energy {:e}     [J]".format(self.getEV(),        self.getEJ() ) )
        print( "Total Mass   {:e} [kg]                                 ".format(self.getMass() ) )
        print( "Abs Momentum {:e} [kg*m/s]                             ".format(self.getAbsMoment()) )
        print( "frequency    {:e} [Hz]        omega        {:e} [2Pi/s]".format(self.getFreq(),      self.getOmega()  ) )
        print( "wavelength   {:e} [m]         wave number  {:e} [2Pi/m]".format(self.getLambda(),    self.getWaveNum()) )
        print( "=======================================================================" )
        
#------------------------------------------------------------------------------
print('PartCommon class ver 0.20')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
