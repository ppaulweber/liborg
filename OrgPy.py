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


#==============================================================================
# OPTIONS
#==============================================================================

class OrgModeOption( object ) :
    pass
# end class


#==============================================================================
# ORGMODE CONTENT (BASE CLASS)
#==============================================================================

class OrgModeContent :
    def __init__( self, line = None ) :
        self._line    = line
        self._options = []
        self._content = []
    # end def
    
    def __str__( self ) :
        return "%s: %s, %s" % (self.__class__.__name__, self._line, self._options, )
    # end def
    
    def append( self, content ) :
        assert( isinstance( content, OrgModeContent ) )
        self._content.append( content )
    # end def

    def pop( self ) :
        return self._content.pop()
    # end def
    
    def peek( self ) :
        try :
            return self._content[-1]
        except IndexError:
            return None
    # end def
    
    def add( self, option ) :
        assert( isinstance( option, OrgModeOption ) )
        self._options.append( option )
    # end def
    
    def dump( self, indent = 0 ) :    
        ind = ""
        for i in range( indent ) :
            ind = "%s " % ind
        
        printf( "%s%s", ind, self ) 
        
        for c in self._content :
            c.dump( indent+1 )
    # end def
# end class


#==============================================================================
# HEADING AND SECTIONS
#==============================================================================

class Heading( OrgModeContent ) :
    def __init__( self, line, depth ) :
        OrgModeContent.__init__( self, line )
        self.depth = depth
    # end def

    def __str__( self ) :
        return "%s @ %s" % ( OrgModeContent.__str__( self ), self.depth )
    # end def
# end class


#==============================================================================
# PARAGRAPH
#==============================================================================

class Paragraph( OrgModeContent ) :
    def __init__( self ) :
        OrgModeContent.__init__( self )
    # end def
# end class

class ParagraphLine( OrgModeContent ) :
    def __init__( self, line ) :
        OrgModeContent.__init__( self, line )
    # end def

    def append( self, content ) :
        assert( isinstance( content, Paragraph ) )
        self._content.append( content )
    # end def
# end class


#==============================================================================
# TABLE
#==============================================================================

class Table( OrgModeContent ) :
    def __init__( self ) :
        OrgModeContent.__init__( self )
    # end def

    def append( self, content ) :
        assert( isinstance( content, TableRow ) )
        self._content.append( content )
    # end def
# end class

class TableRow( OrgModeContent ) :
    def __init__( self, line = None ) :
        OrgModeContent.__init__( self, line )
    # end def
# end class

class TableLine( TableRow ) :
    def __init__( self ) :
        TableRow.__init__( self )
    # end def
# end class


#==============================================================================
# LIST
#==============================================================================
        
class List( OrgModeContent ) :
    def __init__( self ) :
        OrgModeContent.__init__( self )
    # end def

    def append( self, content ) :
        assert( isinstance( content, ListItem ) )
        self._content.append( content )
    # end def
# end class

class ListItem( OrgModeContent ) :
    def __init__( self, line ) :
        OrgModeContent.__init__( self, line )
        self.depth = 0 # TODO
    # end def
# end class





class OrgPy :
    
    
    
    def __init__( self, filename, **option ) :
        
        if not os.path.exists( filename ) :
            assert( 0 )
        
        self._filename = filename;
        self._file = []
        
        self._structure = []
        
        orgfile = open( filename, "r" )    
        
        
        
        heading  = re.compile( "^\*+ " )
        
        
        table    = re.compile( "\|-*-\||\|.*\|" )
        column   = re.compile( "\||\+" )
        
        itemize  = re.compile( "-\s|\+\s" )
        
        italic   = re.compile( "/\S+/" )
        bold     = re.compile( "\*\S+\*" )
        link     = re.compile( "(http://\S+)" )
        
        ignore   = re.compile( "[\n]" )
        suppress = re.compile( "\*\*" )
        
        content = OrgModeContent( None )
        
        stack = [ content ]
        
        cnt = 0
        for line in orgfile.readlines() :
            self._file.append( line )
            
            line = ignore.sub( "", line )
             
            h = heading.findall( line )
            if len( h ) > 0 :
                depth = len(h[0])-2
                printf( "%{magenta:%s%}", depth )
                line = line[ depth+2 : ]
                                
                section = Heading( line, depth )
                
                printf( "%{red:%s, \n%s%}", section, stack )


                if isinstance( stack[-1], Heading ) :
                    if depth > stack[-1].depth :
                        printf( "%{Green:>>%}" )
                        stack[-1].append( section )
                        stack.append( section )
                        
                    elif depth < stack[-1].depth :
                        printf( "%{Green:<<%}" )
                        stack.pop()
                        
                        while True :
                            stack.pop()
                            
                            if isinstance( stack[-1], Heading ) :
                                if stack[-1].depth < depth :
                                    break
                            else :
                                break
                        
                        stack[-1].append( section )
                        stack.append( section )
                        
                    else :
                        printf( "%{Green:==%}" )
                        stack.pop()
                        stack[-1].append( section )
                        stack.append( section )
                        
                else :
                    printf( "%{Green:append%}" )
                    stack[-1].append( section )
                    stack.append( section )                        
            
            text = True
            
            line = suppress.sub( "", line )
            
            
            for i in table.finditer( line ) :
                text = False
                last = stack[-1].peek()
                if last is None \
                or not isinstance( last, Table ):
                    stack[-1].append( Table() )
                stack[-1].peek().append( TableRow( line ) )
                printf( "%{yellow:%s%}", i.span() )
                printf( "%{Yellow:%s%}", line[ i.span()[0] : i.span()[1] ].split("|") )
                
            if not text :
                continue

            for i in itemize.finditer( line ) :
                text = False
                last = stack[-1].peek()
                if last is None \
                or not isinstance( last, List ):
                    stack[-1].append( List() )
                stack[-1].peek().append( ListItem( line ) )
                printf( "%{yellow:%s%}", i.span() )
                printf( "%{Yellow:%s%}", line[ i.span()[0] : i.span()[1] ].split("|") )

            if not text :
                continue
            
            if text :
                if len( line ) > 0 :
                    # text found
                    last = stack[-1].peek()
                    if last is None or not isinstance( last, Paragraph ) :
                        stack[-1].append( Paragraph() )
                    
                    stack[-1].peek().append( ParagraphLine( line ) )
            
            #printf( "%-50s%-3i: h=%s", line, cnt, h )
            cnt = cnt + 1
        
        printf( "%s", len( self._file ) )
        
        content.dump()
        
    # end def
        
    def __parse_option( self, line ) :

        for i in italic.finditer( line ) :
            printf( "%{green:%s%}", i.span() )
            
        for i in bold.finditer( line ) :
            printf( "%{yellow:%s%}", i.span() )
                
        for i in link.finditer( line ) :
            printf( "%{blue:%s%}", i.span() )

    # end def
        
# end class
