#==============================================================================
# IUniverse function library
#------------------------------------------------------------------------------
import csv
from math import log2, ceil

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

#==============================================================================
# package's tools
#------------------------------------------------------------------------------

#==============================================================================
# Functions
#------------------------------------------------------------------------------
def surpS( prob ):
    
    # surprise hodnota node je -log2 jeho pravdepodobnosti
    if (prob > 0) and (prob<=1): return -log2(prob)
    else                       : return 0
    
#------------------------------------------------------------------------------
def entrS( prob ):
    
    # entropy je surprise * prob
    if (prob > 0) and (prob<=1): return -log2(prob) * prob
    else                       : return 0
    
#------------------------------------------------------------------------------
def surpA( crd ):
    
    # surprise hodnota node je -log2 jeho pravdepodobnosti
    if crd > 0 : return log2(crd)
    else       : return 0
    
#------------------------------------------------------------------------------
def entrA( crd, prob ):
    
    # entropy je surprise * prob
    if (prob > 0) and (prob<=1): return log2(crd) * prob
    else                       : return 0    

#==============================================================================
# Pascal triangle math
#------------------------------------------------------------------------------
def get_p3n( crd ):
    "combinatoric number N for crd posibilities"
    
    return ceil(log2(crd))

#------------------------------------------------------------------------------
def get_p3nk( n, k ):
    "combinatoric number n over k"
    
    if k  > n: return 0
    if k == n: return 1
    if k == 0: return 1
    if n == 0: return 1
    
    return get_p3nk(n-1, k-1) + get_p3nk(n-1, k)
    
#------------------------------------------------------------------------------
def get_p3( p3n ):
    "returns pascal's triangle in matrix with max(n) = p3n"
    
    # prve dva riadky n = 0, 1
    p3 = [[1],[1,1]]    
    
    # vypocet p3 po riadkoch, od hora nadol n = 2..p3n
    for n in range(2, p3n+1): 
        
        # pridam nasledujuci riadok
        p3.append([])
        
        # lava jednotka k = 0
        p3[n].append(1)     
        
        # kazdy riadok prejdeme zlava doprava k = 1..n-1
        for k in range(1, n): 
            p3[n].append( p3[n-1][k-1] + p3[n-1][k] )

        # prava jednotka k = n
        p3[n].append(1)     
        
    return p3
        
#------------------------------------------------------------------------------
def get_p3bitr( p3n, rank ):
    "entropy in bits based on rank in 2^n posibilities, recursive"
    
    rank +=  1
    bit   = -1
    sum   =  0
    
    while sum < rank: 
        
        bit += 1
        dsm  = get_p3nk( p3n, bit )
        sum += dsm

        # kontrola singularity
        if dsm == 0:
            __journal__( 'ERROR: p3entr({}, {}) is not defined, will be assumed equal {}'.format(p3n, rank, bit+1) ) 
            return bit+1
        
    return bit        
    
#------------------------------------------------------------------------------
def get_p3bit( p3n, rank, p3 ):
    "entropy in bits based on rank in 2^n posibilities, matrix"
    
    rank +=  1
    bit   = -1
    sum   =  0
    
    while sum < rank: 
        
        bit += 1
        dsm  = p3[p3n][bit]
        sum += dsm

        # kontrola singularity
        if dsm == 0:
            __journal__( 'ERROR: p3en({}, {}) is not defined, will be assumed equal {}'.format(p3n, rank, bit+1) ) 
            return bit+1
        
    return bit        
    
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
print('IUniverse library ver 0.01')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
