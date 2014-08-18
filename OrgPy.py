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
import datetime

sys.path.append( "../verbose/python" )

from Verbose import *


log_file = None
log_file = sys.stderr

#==============================================================================
# ORG-MODE STYLES
#==============================================================================

class OrgModeSyntax( object ) :
    prefix  = None
    postfix = None
    
    def __init__( self, prefix, postfix = None ) :
        
        if prefix is None \
        or len( prefix ) == 0 :
            assert( 0 )
        self.prefix  = re.compile( prefix  )
        
        if  postfix is not None :
            if len( postfix ) == 0 :
                assert( 0 )
            self.postfix = re.compile( postfix )
    # end def
# end class

class OrgModeStyle( object ) :

    def __init__( self, position, end_of_style = False ) :
        self._pos = position
        self._end = end_of_style
    # end def
    
    def generate( self, emit, line ) :
        result = line
        text = line[ self._pos[0] : self._pos[1] ]
        
        printf( "%{Yellow:%s%}\n", text, stream = log_file )
        
        if self._end is False :
            # starting style
            if emit[ 0 ] is not None :
                result = "%s%s%s" % \
                ( line[ 0 : self._pos[0] ]
                , emit[ 0 ]( text )
                , line[ self._pos[1] : ] 
                )
        
        else :
            # stopping style
            if emit[ 1 ] is not None :
                result = "%s%s%s" % \
                ( line[ 0 : self._pos[0] ]
                , emit[ 1 ]( text )
                , line[ self._pos[1] : ] 
                )
        
        return result
    # end def
    
    def __repr__( self ) :
        return "%s @ %s: %s" % \
            ( self.__class__.__name__, self._pos, self._end )
    # end def

    def __cmp__( self, other ) :
        assert( isinstance( other, OrgModeStyle ) )
        
        return self._pos[0].__cmp__( other._pos[0] )
    
    _memory = None
    
    @staticmethod
    def fetch( config, line ) :
        
        result = []
        
        if OrgModeStyle._memory is None :
            OrgModeStyle._memory = {}
        
        for style in config.keys() :
            OrgModeStyle._memory[ style ] = False
        
        mem = OrgModeStyle._memory
        
        for i in range( len( line ) ) :
            printf( "%s", i / 10, stream = log_file )
        printf( "\n", stream = log_file )
        for i in range( len( line ) ) :
            printf( "%s", i % 10, stream = log_file )
        printf( "\n", stream = log_file )
            
        for style, syntax in config.iteritems() :
            offset = 0
            cursor = syntax.prefix
            
            if  syntax.postfix is not None \
            and mem[ style ] is not None \
            and mem[ style ] is True :
                cursor = syntax.postfix
            
            while True :
                i = cursor.search( line[ offset : ] )
                
                if i is None :
                    break
                
                pos = \
                ( i.span()[0] + offset
                , i.span()[1] + offset
                )
                
                printf( "%{green:%s%} %s: %s [ %s ]\n"
                     , pos
                     , mem[style]
                     , style, cursor, stream = log_file )
                
                offset = pos[1]
                
                result.append( style( pos, mem[style] ) )
                
                if syntax.postfix is not None :
                    if mem[ style ] :
                        cursor = syntax.prefix
                    else :
                        cursor = syntax.postfix
                
                    mem[ style ] = not mem[ style ]
        
        result = sorted( result, reverse = True )
        
        for style in config.keys() :
            if OrgModeStyle._memory[ style ] is True :
                for r in result :
                    if  r.__class__.__name__ == style.__name__ \
                    and r._end is False :
                        result.remove( r )
                        break
        
        return result
    # end def
# end class

class Italic( OrgModeStyle ) : pass
class Bold( OrgModeStyle ) : pass
class Link( OrgModeStyle ) : pass
class NamedLink( OrgModeStyle ) : pass
class Rule( OrgModeStyle ) : pass
class Footnote( OrgModeStyle ) : pass

ORG_MODE = \
{ Bold        : OrgModeSyntax( "(?<= )\*(?=\S)", "(?<=\S)\*(?= )" )
, Italic      : OrgModeSyntax( "(?<= )/(?=\S)",  "(?<=\S)/(?= )" )
, Link        : OrgModeSyntax( "(?<!\[\[)http://\S*" )
, NamedLink   : OrgModeSyntax( "\[\[http://\S*\]\[\S+\]\]" )
#, Rule        : OrgModeSyntax( "-----{-}*" )
, Footnote    : OrgModeSyntax( "\[fn:\S*:\S*\]" )
}

#==============================================================================
# ORG-MODE CONTENT
#==============================================================================

class OrgModeContent( object ) :
    
    def __init__( self, line = None ) :
        self._line    = line
        self._styles = []
        self._content = []
        
        if line is not None :
            self._styles = OrgModeStyle.fetch( ORG_MODE, line )
            
            for s in self._styles :
                printf( "%{green:%s%} %s: %s\n"
                      , s._pos, s._end, s, stream = log_file )
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
        
        printf( "%s%s\n", ind, self, stream = stream ) 
        
        for c in self._content :
            c.dump( stream, indent+1 )
    # end def

    def generate( self, stream, emit ) :
        
        line = "%s" % self._line
        
        for style in self._styles :
            if style.__class__.__name__ in emit :
                printf( "%{Red:%s%}\n", style, stream = log_file )
                line = style.generate( emit[ style.__class__.__name__ ]
                                     , line )
        
        if self.__class__.__name__ in emit :
            self.generate_pre( stream
                             , emit[ self.__class__.__name__ ]
                             , line )
        
        for content in self._content :
            content.generate( stream, emit )

        if self.__class__.__name__ in emit :
            self.generate_post( stream
                              , emit[ self.__class__.__name__ ]
                              , line )
    # end def
    
    def generate_pre( self, stream, emit, line ) :
        pass
    # end def
    
    def generate_post( self, stream, emit, line ) :
        pass
    # end def
    
# end class


#==============================================================================
# TITLE
#==============================================================================

class Title( OrgModeContent ) :
    #regex = re.compile( "^\*+ " )
    
    def __init__( self, line ) :
        OrgModeContent.__init__( self, line )
    # end def
    
    def __str__( self ) :
        return transform( "%{black,White:%s:%} %s %{yellow:%s%}") % \
            ( OrgModeContent.__str__( self )
            , self._line
            , self._styles )
    # end def
    
    def generate_pre( self, stream, emit, line ) :
        if emit is not None:
            stream.write( unicode( emit( line ) ) )
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
    
    def generate_pre( self, stream, emit, line ) :
        if emit[ 0 ] is not None:
            stream.write( unicode( emit[ 0 ]( self._depth + 1, line ) ) )
    # end def

    def generate_post( self, stream, emit, line ) :
        if emit[ 1 ] is not None:
            stream.write( unicode( emit[ 1 ]( self._depth + 1, line ) ) )
    # end def
    
# end class


#==============================================================================
# PARAGRAPH
#==============================================================================

class Paragraph( OrgModeContent ) :
    def __init__( self, count ) :
        OrgModeContent.__init__( self )
        self._count = count
    # end def
    
    def append( self, content ) :
        assert( isinstance( content, ParagraphLine ) )
        self._content.append( content )
    # end def

    def __str__( self ) :
        return transform( "%s %i" ) % \
            ( OrgModeContent.__str__( self )
            , self._count )
    # end def
    
    def generate_pre( self, stream, emit, line ) :
        if  len( self._content ) > 0 \
        and emit[ 0 ] is not None :
            stream.write( unicode( emit[ 0 ]( self._count ) ) )
    # end def
    
    def generate_post( self, stream, emit, line ) :
        if  len( self._content ) > 0 \
        and emit[ 1 ] is not None :
            stream.write( unicode( emit[ 1 ]( self._count ) ) )
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

    def generate_pre( self, stream, emit, line ) :
        if emit is not None:
            stream.write( unicode( emit( line ) ) )
    # end def

# end class


#==============================================================================
# TABLE
#==============================================================================

class Table( OrgModeContent ) :
    regex = re.compile( "(\|-\s-\|)|(\|\s\|)" )
    
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

    def __str__( self ) :
        return transform( "%{cyan:%s%} %s" ) % \
            ( OrgModeContent.__str__( self )
            , self._line )
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

, "prolog"        : "<!-- prolog -->\n"

, "epilog"        : "<!-- epilog -->\n"

, "Title"         : ( lambda text : "<h1>%s</h1>\n" % text )

, "Heading"       : ( ( lambda depth, line : 
                        "<h%s>%s</h%s>\n" % (depth+1, line, depth+1,) \
                            if depth <= 4 else 
                        "<br><div><b>%s</b></div>\n" % line )
                    , None
                    )

, "Paragraph"     : ( ( lambda cnt : "<div>\n" )
                    , ( lambda cnt : "</div>\n" )
                    )

, "ParagraphLine" : ( lambda line : "%s\n" % line )

, "Bold"          : ( ( lambda text : "<b>" )
                    , ( lambda text : "</b>" )
                    )

, "Italic"        : ( ( lambda text : "<i>" )
                    , ( lambda text : "</i>" )
                    )

, "Link"          : ( ( lambda text : '<a href="%s">%s</a>' % \
                        ( text
                        , re.search( "(?<=://).*", text ).group(0)
                        ) 
                      )
                    , None
                    )

, "NamedLink"     : ( ( lambda text : '<a href="%s">%s</a>' % \
                        ( re.search( "(?<=\[\[).*(?=\]\[)" , text ).group(0)
                        , re.search( "(?<=\]\[).*(?=\]\])" , text ).group(0)
                        ) 
                      )
                    , None
                    )

#, "Rule"          : ( ( lambda text : '<hr>' )
#                    , None
#                    )


, "Footnote"      : ( ( lambda text : '<sup><a href="%s">%s</a></sup>' % \
                        ( re.search( "(?<=:).*(?=:)" , text ).group(0)
                        , re.search( ":.*?:.*?(?=\])", text ).group(0)
                        ) 
                      )
                    , None
                    )

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

, "Paragraph"     : ( ( lambda cnt : "" )
                    , ( lambda cnt : "\n" )
                    )

, "ParagraphLine" : ( lambda line : "%s\n" % line )
}


class OrgPy :
    def __init__( self, filename, configuration = ORG_MODE ) :
        
        self._filename = filename;
        self._content = OrgModeContent( None )
        self._file = []
        
        self._option = \
        { "title" : None
        , "help"  : ""
        }
        
        self._toc  = None
        
        is_file = False

        if isinstance( filename, basestring ) :
            if not os.path.exists( filename ) :
                assert( 0 )
            orgfile = open( filename, "r" )
            is_file = True
            
        elif isinstance( filename, io.StringIO ) :
            orgfile = filename
        
        else :
            assert( 0 )
        
        ignore   = re.compile( "[\n]" )
        suppress = re.compile( "\*\*" )
        
        stack = [ self._content ]
        
        cnt = 0
        par_cnt = 0
        
        for line in orgfile.readlines() :
            self._file.append( line )
            
            line = ignore.sub( "", line )
            
            # check for a heading
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
                printf( "%{cyan:%s -> %s%}\n", line, i.span(), stream = log_file )
                stack[-1].append( Option( line ) )
                text = False
                
                line = line[ (i.span()[1]+1) : ]
                for j in Mark.regex.finditer( line ) :
                    printf( "%{Cyan:%s -> %s%}\n", line, j.span(), stream = log_file )
                    mark = line[ j.span()[0] : j.span()[1] ]
                    line = line[ (j.span()[1]+1) : ]
                    
                    mark = mark[:-1]
                    
                    if mark == "title" :
                        self._option[ mark ] = Title( line )
                        printf( "setting new title '%s'\n" % line, stream = log_file )
                    
                    if mark == "help" :
                        self._option[ mark ] = line
                        printf( "setting new help '%s'\n" % line, stream = log_file )
                    
                    break
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
                    printf( "%s\n", e )
                    
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
                
                title = self._option[ "title" ]
                
                if len( line ) > 0 :
                    if  last is None \
                    and len( stack ) == 1 \
                    and title is None :
                        # title found
                        self._option[ "title" ] = Title( line )
                        title = self._option[ "title" ]
                        stack[-1].append( title )
                        
                    else :
                        # text found
                        if last is None or not isinstance( last, Paragraph ) :
                            par_cnt = 0
                            stack[-1].append( Paragraph( par_cnt ) )
                    
                        stack[-1].peek().append( ParagraphLine( line ) )
                
                else :
                    if  last is None \
                    and len( stack ) == 1 \
                    and title is None :
                        # title found
                        pass
                    else :
                        if  sep == len( line ) \
                        and last is not None \
                        and isinstance( last, Paragraph ) \
                        and len( last._content ) > 0 :
                            par_cnt = par_cnt + 1
                            stack[-1].append( Paragraph( par_cnt ) )
           
            #printf( "%-50s%-3i: h=%s\n", line, cnt, h, stream = log_file )
            cnt = cnt + 1
        

        if is_file :
            orgfile.close()
    # end def
    
    def dump( self, stream = sys.stderr ) :
        printf( "%s\n", len( self._file ), stream = stream )
        self._content.dump( stream )
    # end def
    
    def generate( self, stream = sys.stdout, emit = HTML ) :
        
        if "comment" not in emit \
        or emit[ "comment" ] is None :
            emit[ "comment" ] = ( lambda text : "" )
        
        stream.write( unicode( emit[ "comment" ]( 
                    str( datetime.datetime.utcnow() ) ) ) )
        
        if  "prolog" in emit \
        and emit[ "prolog" ] is not None :
            stream.write( unicode( emit[ "prolog" ] ) )
        
        self._content.generate( stream, emit )
        
        if  "epilog" in emit \
        and emit[ "epilog" ] is not None :
            stream.write( unicode( emit[ "epilog" ] ) )
        
        #print stream
    # end def
    
        
# end class
