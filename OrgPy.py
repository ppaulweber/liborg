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
import io

sys.path.append( "../verbose/python" )

from Verbose import *


log_file = None
#log_file = io.open( ".attic/log", "w" )

#==============================================================================
# ORG-MODE STYLES
#==============================================================================

class OrgModeStyle( object ) :
    prefix  = None
    postfix = None
    
    def __init__( self, prefix, postfix = None ) :
        
        if postfix is None :
            postfix = prefix
        
        if prefix is None \
        or len( prefix ) == 0 :
            assert( 0 )
        
        if postfix is None \
        or len( postfix ) == 0 :
            assert( 0 )
        
        self.prefix  = prefix
        self.postfix = postfix
    # end def
# end class

class Italic( OrgModeStyle ) : pass
#    regex = re.compile( "/\S+/" )
#end class

class Bold( OrgModeStyle ) : pass
#    regex = re.compile( "\*\S+\*" )
# end class

class Link( OrgModeStyle ) : pass
#    regex = re.compile( "(http://\S*)|(https://\S*)|(file://\S*)|(ftp://\S*)")
# end class


ORG_MODE = \
[ Bold( "*" )
, Italic( "/" )
, Link( "s" )
]



#==============================================================================
# ORG-MODE CONTENT
#==============================================================================

class OrgModeContent( object ) :
    
   # _style = [ Italic ] #, Bold, Link ]
    
    def __init__( self, line = None ) :
        self._line    = line
        self._styles = []
        self._content = []
        
        if line is not None :
            pass
            # for e in OrgModeContent._style :
            #     for i in e.regex.finditer( line ) :
            #         printf( "%{green:%s%}\n", i.span(), stream = log_file )
            #         self._styles.append( e() )
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
    
    def dump( self, stream, indent = 0 ) :    
        ind = ""
        for i in range( indent ) :
            ind = "%s " % ind
        
        printf( "%s%s\n", ind, self, stream = log_file ) 
        
        for c in self._content :
            c.dump( stream, indent+1 )
    # end def

    def generate( self, stream, emit ) :
        
        # process line or field!
        
        if self.__class__.__name__ in emit :
            self.generate_pre( stream, emit[ self.__class__.__name__ ] )
        
        for c in self._content :
            c.generate( stream, emit )

        if self.__class__.__name__ in emit :
            self.generate_post( stream, emit[ self.__class__.__name__ ] )
    # end def
    
    def generate_pre( self, stream, emit ) :
        pass
    # end def
    
    def generate_post( self, stream, emit ) :
        pass
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
    
    def generate_pre( self, stream, emit ) :
        if emit[ 0 ] is not None:
            stream.write( unicode( emit[ 0 ]( self._depth + 1, self._line ) ) )
    # end def

    def generate_post( self, stream, emit ) :
        if emit[ 1 ] is not None:
            stream.write( unicode( emit[ 1 ]( self._depth + 1, self._line ) ) )
    # end def
    
# end class


#==============================================================================
# PARAGRAPH
#==============================================================================

class Paragraph( OrgModeContent ) :
    def __init__( self ) :
        OrgModeContent.__init__( self )
    # end def

    def append( self, content ) :
        assert( isinstance( content, ParagraphLine ) )
        self._content.append( content )
    # end def
    
    def generate_pre( self, stream, emit ) :
        if emit[ 0 ] is not None:
            stream.write( unicode( emit[ 0 ]() ) )
    # end def

    def generate_post( self, stream, emit ) :
        if emit[ 1 ] is not None:
            stream.write( unicode( emit[ 1 ]() ) )
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

    def generate_pre( self, stream, emit ) :
        if emit is not None:
            stream.write( unicode( emit( self._line ) ) )
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


#==============================================================================
# ORG-MODE OPTION
#==============================================================================

class Option( OrgModeContent ) :
    regex = re.compile( "#+" )
    
    def __init__( self, line ) :
        OrgModeContent.__init__( self, line )
    # end def
# end class

class Mark( Option ) :
    regex = re.compile( "\S*:" )
    
    def __init__( self, line ) :
        OrgModeContent.__init__( self, line )
    # end def
# end class

# #+MARK{:,_BLOCK {OPTION}}

class Block( Option ) :
    regex     = re.compile( "begin_" )
    regex_end = re.compile( "end_" )
    
    def __init__( self, line ) :
        OrgModeContent.__init__( self, line )
    # end def
    
    def append( self, content ) :
        assert( isinstance( content, ListItem ) )
        self._content.append( content )
    # end def
# end class

# class Source( Block ) :
#     regex = re.compile( "src" )
    
#     def __init__( self, line ) :
#         OrgModeContent.__init__( self, line )
#     # end def
    
#     def append( self, content ) :
#         assert( isinstance( content, ParagraphLine ) )
#         self._content.append( content )
#     # end def
# # end class


#==============================================================================
# ORG-PY
#==============================================================================


HTML = \
{ "comment"       : ( lambda text : "<!-- %s -->\n" % text )

, "Heading"       : ( ( lambda depth, line : 
                        "<h%s>%s</h%s>\n" % (depth, line, depth) if depth <= 4 else 
                        "<br><div><b>%s</b></div>\n" % line )
                    , None
                    )

, "Paragraph"     : ( ( lambda : "<div>\n" )
                    , ( lambda : "</div>\n" )
                    )

, "ParagraphLine" : ( lambda line : "%s\n" % line )
}

LATEX = \
{ "comment"       : ( lambda text : "%%%%%% %s\n" % text )

, "Heading"       : ( ( lambda depth, line : 
                        "\section{%s}\n"       % line if depth == 1 else
                        "\subsection{%s}\n"    % line if depth == 2 else
                        "\subsubsection{%s}\n" % line if depth == 3 else
                        "\paragraph{%s}\n"     % line if depth == 4 else
                        #"\subparagraph{%s}\n"  % line if depth == 5 else
                        "TODO\n" )
                    , None
                    )

, "Paragraph"     : ( ( lambda : "" )
                    , ( lambda : "\n" )
                    )

, "ParagraphLine" : ( lambda line : "%s\n" % line )
}


class OrgPy :
    def __init__( self, filename, configuration = ORG_MODE ) :
        
        
        self._filename = filename;
        self._content = OrgModeContent( None )
        self._file = []
        
        if isinstance( filename, basestring ) :
            if not os.path.exists( filename ) :
                assert( 0 )
            orgfile = open( filename, "r" )

        elif isinstance( filename, io.StringIO ) :
            orgfile = filename

        else :
            assert( 0 )
        
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
                printf( "%{magenta:%s%}\n", depth, stream = log_file )
                line = line[ depth+2 : ]
                                
                section = Heading( line, depth )
                
                printf( "%{red:%s, \n%s%}\n", section, stack, stream = log_file )
                
                
                if isinstance( stack[-1], Heading ) :
                    if depth > stack[-1]._depth :
                        printf( "%{Green:>>%}\n", stream = log_file )
                        stack[-1].append( section )
                        stack.append( section )
                        
                    elif depth < stack[-1]._depth :
                        printf( "%{Green:<<%}", stream = log_file )
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
                        printf( "%{Green:==%}\n", stream = log_file )
                        stack.pop()
                        stack[-1].append( section )
                        stack.append( section )
                        
                else :
                    printf( "%{Green:append%}\n", stream = log_file )
                    stack[-1].append( section )
                    stack.append( section )                        
                continue
            
            
            text = True
            line = suppress.sub( "", line )
            
            
            for i in Option.regex.finditer( line ) :
                stack[-1].append( Option( line ) )
                printf( "%{cyan:%s -> %s%}\n", line, i.span(), stream = log_file )
                text = False
                break
            
            if not text :
                continue
            
            
            elements = [ (Table,  TableRow)
                       , (List,   ListItem)
                       ]
            
            for e in elements :
                for i in e[0].regex.finditer( line ) :
                    text = False
                    last = stack[-1].peek()
                    if last is None \
                    or not isinstance( last, e[0] ) :
                        stack[-1].append( e[0]() )
                    
                    stack[-1].peek().append( e[1]( line ) )
                    printf( "%{yellow:%s%}\n", i.span(), stream = log_file )
                    printf( "%{Yellow:%s%}\n"
                          , line[ i.span()[0] : i.span()[1] ].split("|")
                          , stream = log_file )
                    
                if not text :
                    break 
            if not text :
                continue
            
            if text :
                sep = line.count( " " )
                sep = sep + line.count( "\t" )
                sep = sep + line.count( "\n" )
                
                printf( "%{Blue:%s %{red,bold:%s%}%} -> %s\n"
                      , line, text, sep, stream = log_file )
                
                last = stack[-1].peek()
                
                if len( line ) > 0 :
                    # text found                
                    if last is None or not isinstance( last, Paragraph ) :
                        stack[-1].append( Paragraph() )
                    
                    stack[-1].peek().append( ParagraphLine( line ) )

                else :
                    if  sep == len( line ) \
                    and last is not None \
                    and isinstance( last, Paragraph ) :
                        stack[-1].append( Paragraph() )
            
            #printf( "%-50s%-3i: h=%s\n", line, cnt, h, stream = log_file )
            cnt = cnt + 1
        
        
    # end def
    
    def dump( self, stream = sys.stderr ) :
        printf( "%s\n", len( self._file ), stream = log_file )
        self._content.dump( stream )
    # end def
    
    def generate( self, stream = sys.stdout, emit = HTML ) :
        
        if "comment" not in emit \
        or emit[ "comment" ] is None :
            emit[ "comment" ] = ( lambda text : "" )
        
        from datetime import datetime
        
        stream.write( unicode( emit[ "comment" ]( str( datetime.utcnow() ) ) ) )
        
        
        self._content.generate( stream, emit )
        
        #print stream
    # end def
    
        
# end class
