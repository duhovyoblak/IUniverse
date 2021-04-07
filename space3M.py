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
from siqo_lib      import journal
from iuniverse_lib import _ERR, _C, _C2

from math          import sqrt, exp, sin, cos
import cmath       as cm

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

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
        
        self.name  = name     # unique name for Minkowski space in Your project
        self.shape = {}       # grid's shape as {xMin, xMax, yMin, yMax, zMin, zMax, tMin, tMax}
        self.base  = {}       # {id:cell}  id='<name>#gx#gy#gz#gt' cell={pos:{}, val:{}, opt:{}}
        self.blur  = {}       # {id:cell}  id='<name>#gx#gy#gz#gt' cell={pos:{}, val:{}, opt:{}}
        self.parts = {}       # {'part.name':part} all of particles in space
        self.mpg   = 1        # meters  per 1 grid distance
        self.spg   = 1        # seconds per 1 grid distance
        
        self.clear()           # reset all parameters

        journal.O( 'Space3M {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        # Vycisti zoznam bodov v oboch dictionaries
        self.base.clear()
        self.blur.clear()
        self.setAct('base')
        
        self.shape = {'xMin':0, 'xMax':0, 'yMin':0, 'yMax':0, 'zMin':0, 'zMax':0, 'tMin':0, 'tMax':0}

        # Vycisti zoznam castic a nastavi zoom
        self.parts.clear()
        self.setZoom(1)

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
        
        dt2 = dt*dt
        dr2 = dx*dx + dy*dy +dz*dz
        
        return { 'dx' :dx,  'dy':dy, 'dz':dz, 'dt':dt, 
                 'dr2':dr2, 'dr':sqrt(dr2),  'dt2':dt2, 
                 'cDs':cm.sqrt(dr2 - _C2*dt2), 'cDt':cm.sqrt(dt2 - dr2/_C2) }
        
    #--------------------------------------------------------------------------
    def getGridInt(self, ga, gb):
        "Return metric between two grid positions in eucleidian grid distance"

        dx = gb['x']-ga['x']
        dy = gb['y']-ga['y']
        dz = gb['z']-ga['z']
        dt = gb['t']-ga['t']
        
        return { 'dx':dx, 'dy':dy, 'dz':dz, 'dt':dt, 'dG':sqrt(dx*dx + dy*dy +dz*dz + dt*dt)}

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
            journal.M( 'Space3M {} getIdStruct ERROR id={}'.format(self.name, id), 0)
            return toret

    #--------------------------------------------------------------------------
    def addCellByGrid(self, grid, opt={}):
        "Create and append cell into active dictionary for given grid position"
        
        pos  = self.getPos(grid)
        id   = self.getIdFromGrid(grid)
        dPos = self.getPosInt(0, pos)
        
        cell = {'pos': pos, 
                'val': { 'cDs':dPos['cDs'], 'cDt':dPos['cDt'], 'phi':dPos['dt']-sqrt(dPos['dr2']), 'cAmp':complex(0,0) },
                'opt': opt }

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
            toret = self.addCellById(id, opt)
        
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
            p = cell['pos']
            v = cell['val']
            
            print('----------------------------------------------------------------------------------------------------')
            print( "Cell ID = {}".format(id) )
            print( "  x = {:e},                 y = {:e},                 z = {:e}, t = {:e}".format(p['x'], p['y'], p['z'] ,p['t']) )
            print( "cDs = {:e}, cDt = {:e}, phi = {:e}".format( v['cDs'], v['cDt'], v['phi'] ) )
        
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
        
        self.shape = shape
        journal.M( 'Space3M {} shape is {}'.format(self.name, self.shape), 10)
        
        # Create grid shape
        i = 0
        for ix in range(shape['xMin'], shape['xMax']):
            for iy in range(shape['yMin'], shape['yMax']):
                for iz in range(shape['zMin'], shape['zMax']):
                    for it in range(shape['tMin'], shape['tMax']):
                        
                        grid = {'x':ix, 'y':iy, 'z':iz, 't':it}
                        self.addCellByGrid(grid)
                        i   += 1
        
        journal.O( 'Space3M {} created {} cells'.format(self.name, str(i)), 10)

    #--------------------------------------------------------------------------
    def partToSpace(self, part ):
        "Append phi for given particle for every ID in the Space"
        
        partPos = part.getPos()
        
        i=0
        for cell in self.act.values():
            
            # ziskanie pootocenia amplitudy
            dPos = self.getPosInt( partPos, cell['pos'] )
            phi  = part.getPhi(dPos)
            cAmp = cm.exp(complex(0,phi))
            
            # pokles amplitudy so vzdialenostou
            r    = abs(dPos['cDt'])
            if r < 1e-9: r = 1e-9
            cAmp = cAmp / r
        
            # superpozicia do priestoru
            cell['val']['cAmp'] = cell['val']['cAmp'] + cAmp
            i += 1

        journal.M( 'Space3M {} partToSpace for {} applied for {} cells'.format(self.name, part.getName(), i), 10)

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
        
        #----------------------------------------------------------------------
        # Metadata section
        meta = { 
                 'gx'    :{'dim':'grid'   , 'unit':'', 'coeff':1, 'min':self.shape['xMin'], 'max':self.shape['xMax']},
                 'gy'    :{'dim':'grid'   , 'unit':'', 'coeff':1, 'min':self.shape['yMin'], 'max':self.shape['yMax']},
                 'gz'    :{'dim':'grid'   , 'unit':'', 'coeff':1, 'min':self.shape['zMin'], 'max':self.shape['zMax']},
                 'gt'    :{'dim':'grid'   , 'unit':'', 'coeff':1, 'min':self.shape['tMin'], 'max':self.shape['tMax']},
                 
                 'x'     :{'dim':'m'      , 'unit':'', 'coeff':1, 'min':0, 'max':0 },
                 'y'     :{'dim':'m'      , 'unit':'', 'coeff':1, 'min':0, 'max':0 },
                 'z'     :{'dim':'m'      , 'unit':'', 'coeff':1, 'min':0, 'max':0 },
                 't'     :{'dim':'s'      , 'unit':'', 'coeff':1, 'min':0, 'max':0 },
                 
                 'reDs'  :{'dim':'m.re'   , 'unit':'', 'coeff':1},
                 'imDs'  :{'dim':'m.im'   , 'unit':'', 'coeff':1},
                 'abDs'  :{'dim':'m'      , 'unit':'', 'coeff':1},

                 'phi'   :{'dim':'rad'    , 'unit':'', 'coeff':1},

                 'reDt'  :{'dim':'s.re'   , 'unit':'', 'coeff':1},
                 'imDt'  :{'dim':'s.im'   , 'unit':'', 'coeff':1},
                 'abDt'  :{'dim':'s'      , 'unit':'', 'coeff':1},
                 
                 'reAmp' :{'dim':'Amp.re' , 'unit':'', 'coeff':1},
                 'imAmp' :{'dim':'Amp.im' , 'unit':'', 'coeff':1},  
                 'abAmp' :{'dim':'Amp'    , 'unit':'', 'coeff':1},  
                 'P'     :{'dim':'real'   , 'unit':'', 'coeff':1}  
               }
        
        #----------------------------------------------------------------------
        # Data section
        data = {'gx'   :[], 'gy'   :[],    'gz':[], 'gt':[], 
                'x'    :[], 'y'    :[],    'z' :[], 't' :[], 
                'reDt' :[], 'imDt' :[], 'abDt' :[],
                'phi'  :[],
                'reDs' :[], 'imDs' :[], 'abDs' :[],
                'reAmp':[], 'imAmp':[], 'abAmp':[], 'P' :[] }
        
        toret = { 'meta':meta, 'data':data }
        
        i = 0
        for id, cell in self.act.items():
            
            rec  = self.getIdStruct(id)
            
            toret['data']['gx'   ].append(     int(rec['x'   ])      )
            toret['data']['gy'   ].append(     int(rec['y'   ])      )
            toret['data']['gz'   ].append(     int(rec['z'   ])      )
            toret['data']['gt'   ].append(     int(rec['t'   ])      )
            
            toret['data']['x'    ].append( cell['pos']['x'   ]       )
            toret['data']['y'    ].append( cell['pos']['y'   ]       )
            toret['data']['z'    ].append( cell['pos']['z'   ]       )
            toret['data']['t'    ].append( cell['pos']['t'   ]       )
            
            toret['data']['reDs' ].append( cell['val']['cDs' ].real  )
            toret['data']['imDs' ].append( cell['val']['cDs' ].imag  )
            toret['data']['abDs' ].append( abs(cell['val']['cDs'])   )

            toret['data']['phi'  ].append( cell['val']['phi' ]       )

            toret['data']['reDt' ].append( cell['val']['cDt' ].real  )
            toret['data']['imDt' ].append( cell['val']['cDt' ].imag  )
            toret['data']['abDt' ].append( abs(cell['val']['cDt'])   )
            
            toret['data']['reAmp'].append( cell['val']['cAmp'].real  )
            toret['data']['imAmp'].append( cell['val']['cAmp'].imag  )
            
            abAmp =  abs(cell['val']['cAmp'])
            toret['data']['abAmp'].append( abAmp                     )
            toret['data']['P'    ].append( abAmp * abAmp             )
            i +=1
        
        #----------------------------------------------------------------------
        # Aggregation section
        
        pX = list(toret['data']['x'])
        pX.sort()
        pY = list(toret['data']['y'])
        pY.sort()
        pZ = list(toret['data']['z'])
        pZ.sort()
        pT = list(toret['data']['t'])
        pT.sort()
        
        toret['meta']['x']['min'] = pX[ 0]
        toret['meta']['x']['max'] = pX[-1]
        toret['meta']['y']['min'] = pY[ 0]
        toret['meta']['y']['max'] = pY[-1]
        toret['meta']['z']['min'] = pZ[ 0]
        toret['meta']['z']['max'] = pZ[-1]
        toret['meta']['t']['min'] = pT[ 0]
        toret['meta']['t']['max'] = pT[-1]
        
        journal.M( 'Space3M {} getPlotData created {} records'.format(self.name, i), 10)
        return toret
    
#------------------------------------------------------------------------------
print('Minkowski space class ver 0.35')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
