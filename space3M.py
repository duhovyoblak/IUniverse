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

from math     import sqrt, exp, sin, cos

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

_ERR            = '_ERROR_'

_PI             = 3.141592653589793    # Pi number
_2PI            = 6.283185307179586
_SQRT_2PI       = 2.5066282746310002
_REV_SQRT_2PI   = 0.3989422804014327

_E              = 2.718281828459045    # Euler number
_H              = 6.62607015e-34       # Planck quantum in [Joule*second]
_H_RED          = _H / _2PI            # Reduced Planck quantum
_C              = 299792458            # speed of light in [meter/second]
_C2             = _C * _C              # speed of light square

#==============================================================================
# package's tools
#-------------------------- ----------------------------------------------------


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
        
        self.name  = name                 # unique name for Minkowski space in Your project
        
        self.setZoom(10)
        self.mpg   = 1                    # meters  per 1 grid distance
        self.spg   = 1                    # seconds per 1 grid distance
        
        self.setZoom(10)                  # reset mpg and spg parameters

        self.base  = {}  # {id:cell}  id='<name>#gx#gy#gz#gt' cell={pos:{}, val:{}, opt:{}}
        self.blur  = {}  # {id:cell}  id='<name>#gx#gy#gz#gt' cell={pos:{}, val:{}, opt:{}}

        self.act   = self.setAct('base')  # Active dictionary = all methods use this data
        
        self.parts = {}                   # {'part.name':part} all of particles in space

        journal.O( 'Space3M {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        self.base.clear()
        self.blur.clear()

        self.setAct('base')
        
        self.parts.clear()

        self.mpg  = 1                 # meters  per 1 grid distance
        self.spg  = self.mpg / _C     # seconds per 1 grid distance

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

    #--------------------------------------------------------------------------
    def setZoom(self, mpg, spg=0):
        "Set meters per grid and seconds per grid parameters"

        self.mpg = mpg
        
        if spg == 0 : self.spg = mpg / _C
        else        : self.spg = spg

        journal.M( 'Space3M {} setted {} meters_per_grid and {} seconds_per_grid'.format(self.name, self.mpg, self.spg), 10)
        
    #==========================================================================
    # Tools for grid_to_real_position transformations, no data changed or referenced
    #--------------------------------------------------------------------------
    def getGrid(self, pos):
        "Return nearest grid position (indices for numpy arrays) for given real position"

        gx = int(round(pos['x'] / self.mpg))
        gy = int(round(pos['y'] / self.mpg))
        gz = int(round(pos['z'] / self.mpg))
        gt = int(round(pos['t'] / self.spg))

        return {'x':gx, 'y':gy, 'z':gz, 't':gt}

    #--------------------------------------------------------------------------
    def getPos(self, grid):
        "Return real position for given grid position (indices for numpy arrays)"

        x = grid['x'] * self.mpg
        y = grid['y'] * self.mpg
        z = grid['z'] * self.mpg
        t = grid['t'] * self.spg

        return {'x':x, 'y':y, 'z':z, 't':t}

    #--------------------------------------------------------------------------
    def getPosInt(self, pa, pb):
        "Return metric between two real positions (pb-pa) in space-time interval"

        if pa==0: pa = {'x':0, 'y':0, 'z':0, 't':0}

        dx = pb['x']-pa['x']
        dy = pb['y']-pa['y']
        dz = pb['z']-pa['z']
        dt = pb['t']-pa['t']

        dt2 = _C2*dt*dt
        dl2 = dx*dx + dy*dy +dz*dz
        
        re, im = 0, 0

        if dt2 > dl2: re = sqrt( dt2 - dl2 )
        else        : im = sqrt( dl2 - dt2 )

        return { 'dx':dx, 'dy':dy, 'dz':dz, 'dt':dt, 're':re, 'im':im }

    #--------------------------------------------------------------------------
    def getGridInt(self, ga, gb):
        "Return metric between two grid positions in eucleidian grid distance"

        dx = gb['x']-ga['x']
        dy = gb['y']-ga['y']
        dz = gb['z']-ga['z']
        dt = gb['t']-ga['t']
        
        return { 'dx':dx, 'dy':dy, 'dz':dz, 'dt':dt, 'int':sqrt(dx*dx + dy*dy +dz*dz + dt*dt)}

    #==========================================================================
    # Tools for cell's selecting, creating & editing
    #--------------------------------------------------------------------------
    def getIdFromGrid(self, grid):
        "Create cell's ID from grid position"
        
        return self.name+ '#' +str(grid['x'])+'#'+str(grid['y'])+'#'+str(grid['z'])+'#'+str(grid['t'])

    #--------------------------------------------------------------------------
    def getIdFromPos(self, pos):
        "Create cell's ID from real position"
        
        grid = self.getGrid(pos)
        return self.getIdFromGrid(grid)

    #--------------------------------------------------------------------------
    def getIdStruct(self, id):
        "Return ID's structure"
        
        toret = { 'name':_ERR }
        
        try:
            l = id.split('#')
            
            toret['name'] = l[0]
            toret['x'   ] = l[1]
            toret['y'   ] = l[2]
            toret['z'   ] = l[3]
            toret['t'   ] = l[4]
            return toret
            
        except:
            journal( 'Space3M {} getIdStruct ERROR id={}'.format(self.name, id), 0)
            return toret

    #--------------------------------------------------------------------------
    def addCellByGrid(self, grid, opt={}):
        "Create and append cell into active dictionary for given grid position"
        
        pos  = self.getPos(grid)
        id   = self.getIdFromGrid(grid)
        dP   = self.getPosInt(0, pos)
        
        cell = {'pos':pos, 
                'val':{ 'reDs':dP['re'], 'imDs':dP['im'], 'phi':0, 'phs':0, 'amp':0}, 'opt':opt }

        self.act[id] = cell
        
        return cell
        
    #--------------------------------------------------------------------------
    def addCellById(self, id, opt={}):
        "Create and append cell into active dictionary for given ID"
        
        rec  = self.getIdStruct(id)
        grid = (rec['x'], rec['y'], rec['z'], rec['t'])
            
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

    #==========================================================================
    # Tools for editing of particles
    #--------------------------------------------------------------------------
    def addPart(self, part):
        "Add already existing particle into space"
        
        self.parts[part.getName()] = part
        
        journal.M( "Space3M {} added Particle '{}'".format(self.name, part.getName()), 10)
        
    #--------------------------------------------------------------------------
    def printCell(self, id):
        "Print cell for given ID with their properties"
        
        try: 
            cell = self.act[id]
            
            print( id, cell['pos'], cell['val'], cell['opt'] )
        
        except KeyError:
            journal.M( "Space3M {} can't print cell ID = {}. No such cell".format(self.name, id), 9)
        
    #--------------------------------------------------------------------------
    def printParts(self):
        "Print list of particles with theirs properties"
        
        i = 1
        for part in self.parts.values():
            
            print()
            print("Particle {}".format(i))
            part.print()
            i += 1
            
    #--------------------------------------------------------------------------
    #==========================================================================
    # Tools for Space initialisation & editing
    #--------------------------------------------------------------------------
    def createSpace(self, shape, mpg, spg=0 ):
        "Create grid {xMin, xMax, yMin, yMax, zMin, zMax, tMin, tMax} with given meters_per_grid"
        
        journal.I( 'Space3M {} createSpace...'.format(self.name), 10)

        self.clear()
        self.setZoom(mpg, spg)
        
        # Create grid shape
        i = 0
        for ix in range(shape['xMin'], shape['xMax']):
            for iy in range(shape['yMin'], shape['yMax']):
                for iz in range(shape['zMin'], shape['zMax']):
                    for it in range(shape['tMin'], shape['tMax']):
                        
                        grid = {'x':ix, 'y':iy, 'z':iz, 't':it}
                        cell = self.addCellByGrid(grid)
                        i   += 1
        
        journal.O( 'Space3M {} created {} cells'.format(self.name, str(i)), 10)

    #--------------------------------------------------------------------------
    def partToSpace(self, part ):
        "Append phi for given particle for every ID in the Space"
        
        om = part.getOmega()
        kv = part.getWaveVec()
        pp = part.getPos()
        
        for cell in self.act.values():
            
            dP  = self.getPosInt( pp, cell['pos'] )
            phi = om*dP['dt'] - abs( kv['x']*dP['dx'] + kv['y']*dP['dy'] + kv['z']*dP['dz'] )
            
            cell['val']['phi'] += phi
            cell['val']['phs']  = cell['val']['phi'] % _2PI

        journal.M( 'Space3M {} partToSpace for {}'.format(self.name, part.getName()), 10)

    #--------------------------------------------------------------------------
    def partsUp(self):
        "Call partToSpace() for all praticles in the list"
        
        journal.I( 'Space3M {} partsUp...'.format(self.name), 10)

        for part in self.parts.values():

            self.partToSpace(part)
            
        journal.O( 'Space3M {} partsUp done'.format(self.name), 10)

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
        
        # Metadata section
        meta = { 'x'    :{'dim':'m'   , 'unit':'', 'coeff':1},
                 'y'    :{'dim':'m'   , 'unit':'', 'coeff':1},
                 'z'    :{'dim':'m'   , 'unit':'', 'coeff':1},
                 't'    :{'dim':'s'   , 'unit':'', 'coeff':1},
                 'reDs' :{'dim':'s'   , 'unit':'', 'coeff':1},
                 'imDs' :{'dim':'im s', 'unit':'', 'coeff':1},
                 'phi'  :{'dim':'rad' , 'unit':'', 'coeff':1},
                 'phs'  :{'dim':'rad' , 'unit':'', 'coeff':1},
                 'phs_x':{'dim':''    , 'unit':'', 'coeff':1},
                 'phs_y':{'dim':''    , 'unit':'', 'coeff':1}  }
        
        # Data section
        data = {'x':[], 'y':[], 'z':[], 't':[],'reDs':[],'imDs':[],
                'phi':[], 'phs':[], 'phs_x':[], 'phs_y':[] }
        
        toret = { 'meta':meta, 'data':data }
        
        for cell in self.act.values():
            
            toret['data']['x'    ].append(     cell['pos']['x'   ]  )
            toret['data']['y'    ].append(     cell['pos']['y'   ]  )
            toret['data']['z'    ].append(     cell['pos']['z'   ]  )
            toret['data']['t'    ].append(     cell['pos']['t'   ]  )
            
            toret['data']['reDs' ].append(     cell['val']['reDs']  )
            toret['data']['imDs' ].append(     cell['val']['imDs']  )
            toret['data']['phi'  ].append(     cell['val']['phi' ]  )
            toret['data']['phs'  ].append(     cell['val']['phs' ]  )
            
            toret['data']['phs_x'].append( sin(cell['val']['phs' ]) )
            toret['data']['phs_y'].append( cos(cell['val']['phs' ]) )
        
        journal.M( 'Space3M {} getPlotData'.format(self.name), 10)
        
        return toret
    
#------------------------------------------------------------------------------
print('Minkowski space class ver 0.22')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
