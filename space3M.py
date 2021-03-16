#==============================================================================
# Minkowski space class
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

        self.base = {}  # {id:cell}  id='<name>#gx#gy#gz#gt' cell={pos:{}, val:{}, opt:{}}
        self.blur = {}  # {id:cell}  id='<name>#gx#gy#gz#gt' cell={pos:{}, val:{}, opt:{}}

        self.act  = self.setAct('base')

        journal.O( 'Space3M {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        self.base.clear()
        self.blur.clear()

        self.setAct('base')

        self.mpg  = 1                 # meters      per 1 grid distance
        self.spg  = self.mpg / _C     # nanoseconds per 1 grid distance

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

        gx = round(self.mpg * pos['x'])
        gy = round(self.mpg * pos['y'])
        gz = round(self.mpg * pos['z'])
        gt = round(self.spg * pos['t'])

        return {'gx':gx, 'gy':gy, 'gz':gz, 'gt':gt}

    #--------------------------------------------------------------------------
    def getPos(self, grid):
        "Return real position for given grid position (indices for numpy arrays)"

        x = grid['gx'] / self.mpg
        y = grid['gy'] / self.mpg
        z = grid['gz'] / self.mpg
        t = grid['gt'] / self.spg

        return {'x':x, 'y':y, 'z':z, 't':t}

    #--------------------------------------------------------------------------
    def getMetPos(self, pa, pb):
        "Return metric between two real positions in space-time interval"

        dx = pb['x']-pa['x']
        dy = pb['y']-pa['y']
        dz = pb['z']-pa['z']
        dt = pb['t']-pa['t']

        return { 'dx':dx, 'dy':dy, 'dz':dz, 'dt':dt, 'met':sqrt(dx*dx + dy*dy +dz*dz - _C2*dt*dt)}

    #--------------------------------------------------------------------------
    def getMetGrid(self, ga, gb):
        "Return metric between two grid positions in eucleidian grid distance"

        dx = gb['gx']-ga['gx']
        dy = gb['gy']-ga['gy']
        dz = gb['gz']-ga['gz']
        dt = gb['gt']-ga['gt']

        return { 'dx':dx, 'dy':dy, 'dz':dz, 'dt':dt, 'met':sqrt(dx*dx + dy*dy +dz*dz + dt*dt)}

    #==========================================================================
    # Tools for cell's selecting, creating & editing
    #--------------------------------------------------------------------------
    def getIdFromGrid(self, grid):
        "Create cell's ID from grid position"
        
        return self.name+ '#' +str(grid['gx'])+'#'+str(grid['gy'])+'#'+str(grid['gz'])+'#'+str(grid['gt'])

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
    def addCellByGrid(self, grid, opt={}):
        "Create and append cell into active dictionary for given grid position"
        
        pos  = self.getPos(grid)
        id   = self.getIdFromGrid(grid)
        cell = {'pos':pos, 'val':{'phi':0, 'phs':0, 'amp':0}, 'opt':opt }

        self.act[id] = cell
        
        return cell
        
    #--------------------------------------------------------------------------
    def addCellById(self, id, opt={}):
        "Create and append cell into active dictionary for given ID"
        
        rec  = self.getIdParts(id)
        grid = (rec['gx'], rec['gy'], rec['gz'], rec['gt'])
            
        return self.addCellByGrid(grid, opt)
        
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
        "Create grid {xMin, xMax, yMin, yMax, zMin, zMax, tMin, tMax} with given meters_per_grid"
        
        journal.I( 'Space3M {} createSpace...'.format(self.name), 10)
        self.clear()

        self.mpg  = mpg               # meters      per 1 grid distance
        self.spg  = self.mpg / _C     # nanoseconds per 1 grid distance
        
        # Create grid shape
        i = 0
        for ix in range(shape['xMin'], shape['xMax']):
            for iy in range(shape['yMin'], shape['yMax']):
                for iz in range(shape['zMin'], shape['zMax']):
                    for it in range(shape['tMin'], shape['tMax']):
                        
                        grid = {'gx':ix, 'gy':iy, 'gz':iz, 'gt':it}
                        cell = self.addCellByGrid(grid)
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
    def getPlotData(self):
        "Create and return numpy arrays for plotting from active dictionary"
        
        toret = {'x':[], 'y':[], 'z':[], 't':[], 'phi':[], 'phase':[]}
        
        for cell in self.act.values():
            
            toret['x'].append( cell['pos']['x'] )
            toret['y'].append( cell['pos']['y'] )
            toret['z'].append( cell['pos']['z'] )
            toret['t'].append( cell['pos']['t'] )
        
        journal.M( 'Space3M {} getPlotData'.format(self.name), 10)
        
        return toret
    
#------------------------------------------------------------------------------
print('Minkowski space class ver 0.10')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
