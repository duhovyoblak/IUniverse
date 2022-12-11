#==============================================================================
# :main file
#------------------------------------------------------------------------------
from siqo_lib      import journal
from space3M       import Space3M
from space3Mgui    import Space3Mgui
from partMassLess  import PartMassLess

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# Functions
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ =='__main__':
  
    journal.I( 'Main loop' )
    
    # Vytvorim testovaci space3M
    st = Space3M('2PhotonsBeat')
    st.createSpace( {'xMin':-30, 'xMax':30, 'yMin':-10, 'yMax':70, 'zMin':0, 'zMax':1, 'tMin':-20, 'tMax':70 }, 0.05 )
    
    # Vytvorim castice
    p = PartMassLess( 'p1', {'x':-0.1, 'y':0, 'z':0, 't':0} )
    p.setLambda(0.5)
    st.addPart(p)

    r = PartMassLess( 'p2', {'x':0.1, 'y':0, 'z':0, 't':0} )
    r.setLambda(0.6)
    st.addPart(r)

    # Superponujem castice do priestoru
    st.partsUp()
    
    # Vytvorim GUI
    gui = Space3Mgui(st)
    
    journal.O('Main end')
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
