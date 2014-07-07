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

sys.path.append( "../verbose/python" )

from Verbose import *

class OrgModeObject :
    pass

class Heading( OrgModeObject ) :
    pass

class Paragraph( OrgModeObject ) :
    pass

class Table( OrgModeObject ) :
    pass

class List( OrgModeObject ) :
    pass

class lal( OrgModeObject ) :
    pass




class OrgPy :
    
    
    
    def __init__( self, filename, **option ) :
        
        if not os.path.exists( filename ) :
            assert( 0 )
        
        self._filename = filename;
        self._file = []
        
        self._structure = []
        
        orgfile = open( filename, "r" )    
        
        
        
        heading = re.compile( "^\*+ " )
        
        
        table   = re.compile( "\|-*-\||\|.*\|" )
        itemize = re.compile( "-\s|\+\s" )
        
        italic  = re.compile( "/\S+/" )
        bold    = re.compile( "\*\S+\*" )
        link    = re.compile( "(http://\S+)" )
        
        ignore  = re.compile( "[\n]|\*\*" )
        
        cnt = 0
        for line in orgfile.readlines() :
            self._file.append( line )
            
            h = heading.findall( line )
            if len( h ) > 0 :
                printf( "%{magenta:%s%}", len(h[0])-1 )
                line = line[ len(h[0]) : ]
            
            line = ignore.sub( "", line )
            
            for i in italic.finditer( line ) :
                printf( "%{green:%s%}", i.span() )
            
            for i in bold.finditer( line ) :
                printf( "%{yellow:%s%}", i.span() )
            
            for i in table.finditer( line ) :
                printf( "%{yellow:%s%}", i.span() )
            
            for i in itemize.finditer( line ) :
                printf( "%{yellow:%s%}", i.span() )
                
            for i in link.finditer( line ) :
                printf( "%{blue:%s%}", i.span() )
            
            printf( "%-50s%-3i: h=%s", line, cnt, h )
            cnt = cnt + 1
        
        printf( "%s", len( self._file ) )
        
    # end def
# end class
