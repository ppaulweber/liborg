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
# STYLES
#==============================================================================

class OrgModeStyle( object ) :
    pass
# end class

class Italic( OrgModeStyle ) :
    regex = re.compile( "/\S+/" )
        
    pass
# end class

class Bold( OrgModeStyle ) :
    regex = re.compile( "\*\S+\*" )
    
    pass
# end class

class Link( OrgModeStyle ) :
    regex = re.compile( "(http://\S*)|(https://\S*)|(file://\S*)|(ftp://\S*)")
    pass
# end class


#==============================================================================
# ORGMODE CONTENT (BASE CLASS)
#==============================================================================

class OrgModeContent( object ) :
    
    _style = [ Italic, Bold, Link ]
    
    def __init__( self, line = None ) :
        self._line    = line
        self._styles = []
        self._content = []
        
        if line is not None :

            for e in OrgModeContent._style :
                for i in e.regex.finditer( line ) :
                    printf( "%{green:%s%}", i.span() )
                    self._styles.append( e() )
    # end def
    
    def __str__( self ) :
        return "%s" % (self.__class__.__name__)
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
    
    def add( self, style ) :
        assert( isinstance( style, OrgModeStyle ) )
        self._styles.append( style )
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
    regex = re.compile( "^\*+ " )
    
    def __init__( self, line, depth ) :
        OrgModeContent.__init__( self, line )
        self._depth = depth
    # end def

    def __str__( self ) :
        return transform( "%{Magenta:%s(%i):%} %s %{yellow:%s%}" ) % \
            ( OrgModeContent.__str__( self )
            , self._depth
            , self._line
            , self._styles )
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
        
    def __str__( self ) :
        return transform( "%{Green:%s:%} %s <TODO> %{yellow:%s%}" ) % \
            ( OrgModeContent.__str__( self )
            , self._line
            , self._styles )
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
    regex = re.compile( "\|-*-\||\|.*\|" )
    
    def __init__( self ) :
        OrgModeContent.__init__( self )
    # end def

    def append( self, content ) :
        assert( isinstance( content, TableRow ) )
        self._content.append( content )
    # end def
# end class

class TableRow( OrgModeContent ) :
    regex = re.compile( "\||\+" )
    
    def __init__( self, line = None ) :
        OrgModeContent.__init__( self, line )
    # end def

    def __str__( self ) :
        return transform( "%{Blue:%s:%} %s <TODO> %{yellow:%s%}" ) % \
            ( OrgModeContent.__str__( self )
            , self._line
            , self._styles )
    # end def
# end class


#==============================================================================
# LIST
#==============================================================================
        
class List( OrgModeContent ) :
    regex = re.compile( "-\s|\+\s" )
    
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
        self._depth = 0 # TODO
    # end def

    def __str__( self ) :
        return transform( "%{Cyan:%s(%i):%} %s <TODO> %{yellow:%s%}" ) % \
            ( OrgModeContent.__str__( self )
            , self._depth
            , self._line
            , self._styles )
    # end def
# end class





class OrgPy :
    
    
    
    def __init__( self, filename, **configuration ) :
        
        if not os.path.exists( filename ) :
            assert( 0 )
        
        self._filename = filename;
        self._content = OrgModeContent( None )
        self._file = []
        
        orgfile = open( filename, "r" )    
        
        
        
        ignore   = re.compile( "[\n]" )
        suppress = re.compile( "\*\*" )
        
        stack = [ self._content ]
        
        cnt = 0
        for line in orgfile.readlines() :
            self._file.append( line )
            
            line = ignore.sub( "", line )
             
            h = Heading.regex.findall( line )
            if len( h ) > 0 :
                depth = len(h[0])-2
                printf( "%{magenta:%s%}", depth )
                line = line[ depth+2 : ]
                                
                section = Heading( line, depth )
                
                printf( "%{red:%s, \n%s%}", section, stack )
                
                
                if isinstance( stack[-1], Heading ) :
                    if depth > stack[-1]._depth :
                        printf( "%{Green:>>%}" )
                        stack[-1].append( section )
                        stack.append( section )
                        
                    elif depth < stack[-1]._depth :
                        printf( "%{Green:<<%}" )
                        stack.pop()
                        
                        while True :
                            stack.pop()
                            
                            if isinstance( stack[-1], Heading ) :
                                if stack[-1]._depth < depth :
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
                continue
            
            text = True
            
            line = suppress.sub( "", line )
            
            elements = [ (Table, TableRow), (List, ListItem) ]
            
            for e in elements :
                for i in e[0].regex.finditer( line ) :
                    text = False
                    last = stack[-1].peek()
                    if last is None \
                    or not isinstance( last, e[0] ):
                        stack[-1].append( e[0]() )
                    stack[-1].peek().append( e[1]( line ) )
                    printf( "%{yellow:%s%}", i.span() )
                    printf( "%{Yellow:%s%}", line[ i.span()[0] : i.span()[1] ].split("|") )

                if not text :
                    break 
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
        
        self._content.dump()
        
    # end def
    
        
# end class
