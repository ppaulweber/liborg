# 
# Copyright (c) 2014 Philipp Paulweber
# 
# This file is part of the 'liborgpy' project which is released under a NCSA
# open source software license. For more information, see the LICENSE.txt 
# file in the project root directory.
#

import sys
import os
import re

sys.path.append( "../libverbose/python" )

from Verbose import *

class OrgPy :
    def __init__( self, filename, **option ) :
        
        if not os.path.exists( filename ) :
            assert( 0 )
        
        orgfile = open( filename, "r" )    
        
        self._file = []
        
        heading = re.compile( "^\*+ " )
        
        italic  = re.compile( "/\S+/" )
        bold    = re.compile( "\*\S+\*" )
        
        ignore = re.compile( "[\n]|//|\*\*" )
        
        cnt = 0
        for line in orgfile.readlines() :
            self._file.append( line )
            
            h = heading.findall( line )
            if len( h ) > 0 :
                line = line[ len(h[0]) : ]
            
            line = ignore.sub( "", line )
            
            for i in italic.finditer( line ) :
                printf( "%{green:%s%}", i.span() )
            
            for i in bold.finditer( line ) :
                printf( "%{yellow:%s%}", i.span() )
            
            printf( "%-50s%-3i: h=%s", line, cnt, h )
            cnt = cnt + 1
        
        printf( "%s", len( self._file ) )
        
    # end def
# end class
