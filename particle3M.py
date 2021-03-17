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
# class Particle3M
#------------------------------------------------------------------------------
class Particle3M:

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name, m, v):
        "Call constructor of Particle3M and initialise it"

        journal.I( 'Particle3M constructor for {}...'.format(name), 10 )
        
        self.name = name       # unique name for particle in Your project
        self.type = 'common'   # type of particle, used in inherited classes
        self.m    = m          # rest mass in [eV/c2]
        self.v    = v          # speed vector {'vx', 'vy', 'vz'} in [meter/second]
        
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
    def getType(self):
        "Return particles's type"
        
        return self.type

    #--------------------------------------------------------------------------
    def setMassKg(self, m):
        "Set rest mass in [eV/c2] for given mass in [kg]"
        
        self.m = m / _EV_KG

    #==========================================================================
    # Physical properties for particle in rest
    #--------------------------------------------------------------------------
    def getPos(self):
        "Return particles's real position"
        
        return self.pos

    #--------------------------------------------------------------------------
    def getMass(self):
        "Return rest mass of particle in [eV/c2]"
        
        return self.m
    
    #--------------------------------------------------------------------------
    def getEnergy(self):
        "Return rest energy of particle in [Joule], E = (mr*1eV) * C2 "
        
        return _EV_KG * self.m * _C2
    
    #==========================================================================
    # Physical properties for (relativistic) moving particle
    #--------------------------------------------------------------------------
    def getAbsV2(self):
        "Return square of abs value of particle's speed, v2 = vx2 + vy2 + vz2"
        
        return self.v['vx']*self.v['vx'] +self.v['vy']*self.v['vy'] +self.v['vz']*self.v['vz']
        
    #--------------------------------------------------------------------------
    def getAbsV(self):
        "Return abs value of particle's speed, v = SQRT( abs(v2) )"
        
        return sqrt( self.getAbsV2() )
        
    #--------------------------------------------------------------------------
    def getMassR(self):
        "Return relativistic mass of particle in [eV/c2], mr = m / sqrt(1 - (v2/c2)) "
        
        try:
            return self.getMass() / sqrt( 1 - self.getAbsV2()/_C2 )
        except:
            journal.M( 'Particle3M {} getMassR is not defined'.format(self.name), 9)
            return _ERR
    
    #--------------------------------------------------------------------------
    def getMomentum(self):
        "Return momentum vector, p = mr * (vx, vy, vz)"
        
        mr = self.getMassR()
        
        return {'px':mr*self.v['vx'], 'py':mr*self.v['vy'], 'pz':mr*self.v['vz']}
        
    #--------------------------------------------------------------------------
    def getEnergyR(self):
        "Return total energy of particle in [Joule], E = (mr*1eV) * C2 "
        
        return _EV_KG * self.getMassR * _C2
    
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
        
        json = {'name':self.name, 'type':self.type, 'm':self.m, 'v':self.v, ' pos':self.pos}
        
        journal.M( 'Particle3M {} getJson created'.format(self.name), 10)
        
        return json
        
    #--------------------------------------------------------------------------
    def print(self):
        "Return list of printable strings with particle's properties"
        
        toret = []
        
        toret.append( "Particle '{}' is type '{}', with rest mass {} eV/c2".format(self.name, self.type, self.m) )
        
        return toret
        
#------------------------------------------------------------------------------
print('Particle class ver 0.10')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
