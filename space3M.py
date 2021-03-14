#==============================================================================
# Minkowski space class
#------------------------------------------------------------------------------
#
#    real position is given in meters for x,z,y and microsecenods for t as real values
#    grid position means position in numpy-like 4D array as integers 0..ix, 0..iy, 0..iz, 0..it
#
#    phi means argument (omega*t - k*x) as real value in radians
#    phs means phi mod 2*PI in radians
#
#------------------------------------------------------------------------------
from siqo_lib import journal

from datetime import datetime
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
_C              = 299.792458           # spped of light in [meter/microsecond]

#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# class Space3M
#------------------------------------------------------------------------------
class Space3M:

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name):
        "Call constructor of Space3M and initialise it with empty data"

        journal.I( 'Space3M constructor for {}...'.format(name), 10 )
        
        self.name = name              # unique name for Minkowski space in Your project
        self.mpg  = 1                 # meters       per 1 grid distance
        self.spg  = self.mpg / _C     # microseconds per 1 grid distance

        self.base = {}  # {id:cell}  id='<name>#gx#gy#gz#gt' cell={pos:(), val:{}, opt:{}}
        self.blur = {}  # {id:cell}  id='<name>#gx#gy#gz#gt' cell={pos:(), val:{}, opt:{}}

        self.act  = self.setAct('base')

        journal.O( 'Space3M {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        self.base.clear()
        self.blur.clear()

        self.setAct('base')

        self.mpg  = 1                 # meters       per 1 grid distance
        self.spg  = self.mpg / _C     # microseconds per 1 grid distance

        journal.M( 'Space3M {} ALL cleared'.format(self.name), 10)
        
    #--------------------------------------------------------------------------
    def setAct(self, typ):
        "Set active data dictionary by type name"

        if typ == 'base': self.act  = self.base
        if typ == 'blur': self.act  = self.blur

        journal.M( 'Space3M {} set active dictionary: {}'.format(self.name, typ), 10)
        
    #--------------------------------------------------------------------------
    def getActType(self):
        "Get type of active data dictionary"

        if self.act == self.base: return 'base'
        if self.act == self.blur: return 'blur'

    #==========================================================================
    # Tools for grid_to_real_position transformations, no data changed or referenced
    #--------------------------------------------------------------------------
    def getGrid(self, pos):
        "Return nearest grid position (indices for numpy arrays) for given real position"

        gx = round(self.mpg * pos[0])
        gy = round(self.mpg * pos[1])
        gz = round(self.mpg * pos[2])
        gt = round(self.spg * pos[3])

        return (gx, gy, gz, gt)

    #--------------------------------------------------------------------------
    def getPos(self, grid):
        "Return real position for given grid position (indices for numpy arrays)"

        x = grid[0] / self.mpg
        y = grid[1] / self.mpg
        z = grid[2] / self.mpg
        t = grid[3] / self.spg

        return (x, y, z, t)

    #--------------------------------------------------------------------------
    def getMetPos(self, pa, pb):
        "Return metric between two real positions in space-time interval"

        dx = pb[0]-pa[0]
        dy = pb[1]-pa[1]
        dz = pb[2]-pa[2]
        dt = pb[3]-pa[3]

        return { 'dx':dx, 'dy':dy, 'dz':dz, 'dt':dt, 'met':sqrt(dx*dx + dy*dy +dz*dz - _C*_C*dt*dt)}

    #--------------------------------------------------------------------------
    def getMetGrid(self, ga, gb):
        "Return metric between two grid positions in eucleidian grid distance"

        dx = gb[0]-ga[0]
        dy = gb[1]-ga[1]
        dz = gb[2]-ga[2]
        dt = gb[3]-ga[3]

        return { 'dx':dx, 'dy':dy, 'dz':dz, 'dt':dt, 'met':sqrt(dx*dx + dy*dy +dz*dz + dt*dt)}

    #==========================================================================
    # Tools for cell's selecting, creating & editing
    #--------------------------------------------------------------------------
    def getIdFromGrid(self, grid):
        "Create cell's ID from grid position"
        
        return self.name+ '#' +str(grid[0])+'#'+str(grid[1])+'#'+str(grid[2])+'#'+str(grid[3])

    #--------------------------------------------------------------------------
    def getIdFromPos(self, pos):
        "Create cell's ID from real position"
        
        grid = self.getGrid(pos)
        return self.getIdFromGrid(grid)

    #--------------------------------------------------------------------------
    def getIdParts(self, id):
        "Return structured parts from cell's ID"
        
        toret = { 'name':_ERR }
        
        try:
            l = id.split('#')
            
            toret['name'] = l[0]
            toret['gx'  ] = l[1]
            toret['gy'  ] = l[2]
            toret['gz'  ] = l[3]
            toret['gt'  ] = l[4]
            return toret
            
        except:
            journal( 'Space3M {} getIdParts ERROR id={}'.format(self.name, id), 0)
            return toret

    #--------------------------------------------------------------------------
    def createCellByGrid(self, grid, opt={}):
        "Create cell in active dictionary for given grid position"
        
        pos  = self.getPos(grid)
        id   = self.getIdFromGrid(grid)
        cell = {'pos':pos, 'val':{'phi':0, 'phs':0, 'amp':0}, 'opt':opt }

        self.act[id] = cell
        
        return cell
        
    #--------------------------------------------------------------------------
    def createCellById(self, id, opt={}):
        "Create cell in active dictionary for given ID"
        
        rec  = self.getIdParts(id)
        grid = (rec['gx'], rec['gy'], rec['gz'], rec['gt'])
            
        return self.createCellByGrid(grid, opt)
        
    #--------------------------------------------------------------------------
    def delCellById(self, id):
        "Delete permanently cell from active data dictionary by ID"

        return self.act.pop(id)

    #--------------------------------------------------------------------------
    def getCellById(self, id, opt={}):
        "Return existing cell by ID or create new cell"

        try: 
            toret = self.act[id]
        
        except KeyError:
            toret = self.createCellById(id, opt)
        
        return toret

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #==========================================================================
    # Tools for Space initialisation
    #--------------------------------------------------------------------------
    def createSpace(self, shape, mpg ):
        "Create empty grid with shape (ix, iy, iz, it) and set transformations for given meters_per_grid"
        
        journal.I( 'Space3M {} createSpace...'.format(self.name), 10)
        self.clear()

        self.mpg  = mpg               # meters       per 1 grid distance
        self.spg  = self.mpg / _C     # microseconds per 1 grid distance
        
        # Create grid shape
        i = 0
        for ix in range(shape[0]):
            for iy in range(shape[1]):
                for iz in range(shape[2]):
                    for it in range(shape[3]):
                        
                        grid = (ix, iy, iz, it)
                        cell = self.createCellByGrid(grid)
                        i   += 1
        
        journal.O( 'Space3M {} created {} cells'.format(self.name, str(i)), 10)

    #==========================================================================
    # Tools for data extraction & persistency
    #--------------------------------------------------------------------------
    def getJson(self):
        "Create and return Json list from active dictionary"
        
        json = []
        
        for id, cell in self.act.items():
            json.append(cell)
        
        journal.M( 'Space3M {} getJson created {} records'.format(self.name, len(json)), 10)
        
        return json
        
    #--------------------------------------------------------------------------
    def getNumpy(self):
        "Create and return numpy 4D array from active dictionary"
        
        journal.M( 'Space3M {} getNumpy'.format(self.name), 10)
    
#------------------------------------------------------------------------------
print('Minkowski space class ver 0.10')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
