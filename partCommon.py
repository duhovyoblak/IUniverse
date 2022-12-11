#==============================================================================
# Common particle in Minkowski space class
#------------------------------------------------------------------------------
#
#    real position is given in meters for x,z,y and nanosecenods for t as real values
#    grid position means position in numpy-like 4D array as integers 0..ix, 0..iy, 0..iz, 0..it
#
#    phi means argument (omega*t - k*x) as real value in radians
#
#------------------------------------------------------------------------------
from siqo_lib      import journal
from iuniverse_lib import _2PI, _C, _C2, _H, _EV_J

from abc           import ABC, abstractmethod
from math          import sqrt, exp


#==============================================================================
# package's constants
#------------------------------------------------------------------------------


#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# class PartCommon
#------------------------------------------------------------------------------
class PartCommon(ABC):

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
    def getPos(self):
        "Return position of probability density amplitude origin"
        
        return self.pos
    
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
        "Return wave number in [2Pi/m], k = 2Pi / lambda"
        
        return _2PI / self.getLambda()
    
    #--------------------------------------------------------------------------
    def getWaveVec(self):
        "Return wave vector in [2Pi/m], kx = ky = kz = k"
        
        # THIS MUST BE RE-DEFINED IN INHERITED CLASS !
        
        return {'x':0, 'y':0, 'z':0}
    
    #==========================================================================
    # Information wave properties
    #--------------------------------------------------------------------------
        
        
    #==========================================================================
    # Tools for Space 
    #--------------------------------------------------------------------------
    @abstractmethod
    def getPhi(self, dPos):
        "Return angle Phi for particle and given interval in Minkowski space"
        
        # THIS MUST BE RE-DEFINED IN INHERITED CLASS !
        
        return 1/0

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
