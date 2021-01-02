#
#   Copyright (C) 2014-2021 Philipp Paulweber
#   All rights reserved.
#
#   Developed by: Philipp Paulweber
#                 <https://github.com/ppaulweber/liborg>
#
#   This file is part of liborg.
#
#   liborg is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   liborg is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with liborg. If not, see <http://www.gnu.org/licenses/>.
#
#   Additional permission under GNU GPL version 3 section 7
#
#   liborg is distributed under the terms of the GNU General Public License
#   with the following clarification and special exception: Linking liborg
#   statically or dynamically with other modules is making a combined work
#   based on liborg. Thus, the terms and conditions of the GNU General
#   Public License cover the whole combination. As a special exception,
#   the copyright holders of liborg give you permission to link liborg
#   with independent modules to produce an executable, regardless of the
#   license terms of these independent modules, and to copy and distribute
#   the resulting executable under terms of your choice, provided that you
#   also meet, for each linked independent module, the terms and conditions
#   of the license of that module. An independent module is a module which
#   is not derived from or based on liborg. If you modify liborg, you
#   may extend this exception to your version of the library, but you are
#   not obliged to do so. If you do not wish to do so, delete this exception
#   statement from your version.
#

import sys
import os
import re
import io
import datetime

sys.path.append( os.path.join( os.path.dirname( __file__ ), "..", "..", "stdhl", "py" ) )

from Verbose import *


log_file = None
#log_file = sys.stderr

#==============================================================================
# ORG-MODE STYLES
#==============================================================================

class OrgModeSyntax( object ) :
    prefix  = None
    postfix = None
    
    def __init__( self
                , prefix
                , postfix = None
                ) :
        
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
    
    def __init__( self
                , position
                , end_of_style = False
                ) :
        
        self._pos = position
        self._end = end_of_style
    # end def
    
    def pipe( self, text, orgpy ) :
        return text
    # end def
    
    def generate( self, emit, line, orgpy ) :
        result = line
        text = line[ self._pos[0] : self._pos[1] ]
        
        printf( "%{Yellow:%s%}\n", text, stream = log_file )
        
        if self._end is False :
            # starting style
            if emit[ 0 ] is not None :
                result = "%s%s%s" % \
                ( line[ 0 : self._pos[0] ]
                , emit[ 0 ]( self.pipe( text, orgpy ) )
                , line[ self._pos[1] : ]
                )
        
        else :
            # stopping style
            if emit[ 1 ] is not None :
                result = "%s%s%s" % \
                ( line[ 0 : self._pos[0] ]
                , emit[ 1 ]( self.pipe( text, orgpy ) )
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

class Bold( OrgModeStyle )      : pass
class Italic( OrgModeStyle )    : pass
class Code( OrgModeStyle )      : pass

class Link( OrgModeStyle )      : 
    def pipe( self, text, orgpy ) :
        protocol = None
        link     = None
        name     = None
        
        if text[0].startswith( "[" ) :
            if "://" in text :
                protocol = re.search( "(?<=\[\[)\S*(?=://)", text ).group(0)
                link     = re.search( "(?<=://)\S*(?=\]\])", text ).group(0)
            elif text.startswith( "[[./" ) :
                protocol = "file"
                link     = re.search( "(?<=\[\[)\S*(?=\]\])", text ).group(0)
            else :
                protocol = None
                link     = re.search( "(?<=\[\[)\S*(?=\]\])", text ).group(0)
                # no protocol means it also could be a reference to TOC entry
                # TODO 
                
            if "][" in link :
                name = re.search( "(?<=\]\[)\S*", link ).group(0)
                link = re.search( "\S*(?=\]\[)", link ).group(0)
            
        else :
            protocol = re.search( "\S*(?=://)",  text ).group(0)
            link     = re.search( "(?<=://)\S*", text ).group(0)
        
        if "://" in text :
            link = "%s://%s" % ( protocol, link )
        
        if name is None :
            name = link
        
        return \
        { "protocol" : protocol
        , "link"     : link
        , "name"     : name
        }
    # end def
# end class

class Rule( OrgModeStyle )      : pass
class Footnote( OrgModeStyle )  : pass

class Input( OrgModeStyle ) :
    def pipe( self, text, orgpy ) :
        text = re.search( "(?<=:)\S*(?=\])", text ).group(0).strip()        
        kind  = re.search( ".*?(?=:)", text ).group(0).strip()
        
        text  = text[ len( kind )+1: ]
        field = re.search( ".*?(?=:)", text ).group(0).strip()
        
        label  = text[ len( field )+1: ]
        
        return \
        { "type"   : kind
        , "name"   : field
        , "value"  : label
        }
    # end def
# end class

class Data( OrgModeStyle ) :
    def pipe( self, text, orgpy ) :
        text = re.search( "(?<=:).*?(?=\])", text ).group(0).strip()
        
        value = None
        query = False
        error = None
        
        if not text.startswith( "{" ) :
            # plain data local loading of a single option element
            opt = orgpy.get_option( text )
            if opt is None :
                error = "(error: invalid '%s' option tag)" % text
            else :
                if isinstance( opt, Title ) :
                    value = opt._line
                else :
                    value = opt.lstrip()
        else :
            # a SQL-based query
            query = True
            if  text.endswith( "}" ) \
            and "}{" in text:
                sql = re.search( "(?<=\{).*?(?=\}\{)", text ).group(0)
                act = re.search( "(?<=\}\{).*?(?=\})", text ).group(0)
                value = ( sql, act )
            else :
                error = "(error: invalid 'data' syntax)"
        
        return \
        { "value"  : value
        , "query"  : query 
        , "error"  : error
        }
    # end def
# end class


ORG_MODE = \
{ Bold        : OrgModeSyntax( "(?<= )\*(?=\S)", "(?<=\S)\*(?= )" )
, Italic      : OrgModeSyntax( "(?<= )/(?=\S)",  "(?<=\S)/(?= )" )
, Code        : OrgModeSyntax( "(?<= )=(?=\S)",  "(?<=\S)=(?= )" )
, Link        : OrgModeSyntax( "((?<!\[\[)\S+://\S*)|(\[\[\S+\]\])" )
#, Rule        : OrgModeSyntax( "-----{-}*" )
, Footnote    : OrgModeSyntax( "\[fn:\S*:\S*\]" )
, Input       : OrgModeSyntax( "\[input:\S+:\S+:\S*\]" )
, Data        : OrgModeSyntax( "\[data:\S*\]" )
}

#==============================================================================
# ORG-MODE CONTENT
#==============================================================================

class OrgModeContent( object ) :
    
    def __init__( self, line = None, style = True ) :
        self._line    = line
        self._styles = []
        self._content = []
        
        if  line is not None \
        and style is True :
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

    def generate( self, stream, emit, orgpy ) :
        
        line = "%s" % self._line
        
        for style in self._styles :
            if style.__class__.__name__ in emit :
                printf( "%{Red:%s%}\n", style, stream = log_file )
                line = style.generate( emit[ style.__class__.__name__ ]
                                     , line
                                     , orgpy
                                     )
        
        if self.__class__.__name__ in emit :
            self.generate_pre( stream
                             , emit[ self.__class__.__name__ ]
                             , line )
        
        for content in self._content :
            content.generate( stream, emit, orgpy )

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
    regex = re.compile( "(\|-)|(\|\s.*\|)" )
    
    def __init__( self ) :
        OrgModeContent.__init__( self )
        self.table = []
        self.columns_max = 0
    # end def
    
    def append( self, content ) :
        assert( isinstance( content, TableRow ) )
        self._content.append( content )
        self.columns_max = max( self.columns_max, len( content.columns ) )
    # end def
    
    def generate_pre( self, stream, emit, line ) :
        if emit[ 0 ] is not None :
            stream.write( unicode( emit[ 0 ]( self.columns_max ) ) )
    # end def
    
    def generate_post( self, stream, emit, line ) :
        if emit[ 1 ] is not None :
            stream.write( unicode( emit[ 1 ]() ) )
    # end def
# end class

class TableRow( OrgModeContent ) :
    regex = re.compile( "\||\+" )
    
    def __init__( self, line = None ) :
        OrgModeContent.__init__( self, line )
        
        col = line.split( "|" )
        col = [ c.strip() for c in col ]
        self.columns = col[ 1:-1 ]
        
        if "---+---" in self.columns[0] :
            self.columns = [ None for c in self.columns[0].split( "-+-" ) ]
            
        l = len( self.columns ) - 1
        i = 0
        for c in self.columns :
            if c is None :
                c = "-+-"
            
            self.append( TableCell( c, i == l ) )
            i = i + 1
    # end def
    
    def __str__( self ) :
        return transform( "%{Blue:%s:%} %s <%s> %{yellow:%s%}" ) % \
            ( OrgModeContent.__str__( self )
            , self._line
            , self.columns
            , self._styles )
    # end def

    def generate_pre( self, stream, emit, line ) :
        if emit is not None:
            stream.write( unicode( emit[ 0 ]() ) )
    # end def

    def generate_post( self, stream, emit, line ) :
        if emit is not None:
            stream.write( unicode( emit[ 1 ]() ) )
    # end def
# end class

class TableCell( OrgModeContent ) :
    def __init__( self, line, isLast ) :
        OrgModeContent.__init__( self, line )
        self._isLast = isLast
    # end def
        
    def __str__( self ) :
        return transform( "%{Magenta:%s:%} %s %{yellow:%s%}" ) % \
            ( OrgModeContent.__str__( self )
            , self._line
            , self._styles )
    # end def
    
    def generate_pre( self, stream, emit, line ) :
        if emit is not None:
            if line == "-+-" :
                line = None
            stream.write( unicode( emit( line, self._isLast ) ) )
    # end def

# end class


#==============================================================================
# LIST
#==============================================================================

#List_stack = None

class List( OrgModeContent ) :
    regex = re.compile( "^(  )*- .*?$" )
    
    _stack = None
    _pos   = None
    
    def __init__( self, depth = 0 ) :
        OrgModeContent.__init__( self )
        self._depth = depth
    # end def
    
    def __str__( self ) :
        return transform( "%{Cyan:%s%}@%s: %s <TODO> %{yellow:%s%}" ) % \
            ( OrgModeContent.__str__( self )
            , self._depth
            , self._line
            , self._styles )
    # end def
    
    def append( self, content ) :
        assert( isinstance( content, ListItem ) )
        
        dep = content._line.find( "- " )
        content._depth = dep;
        
        try :
            last = List._stack[ List._pos ]
        except :
            import pdb; pdb.set_trace()
           
        #printf( "%s =?= %s\n", dep, last._depth, stream = sys.stderr )
        
        if dep > last._depth :
            
            List._pos = dep
            List._stack[ List._pos ] = List( dep )
            
            last._content.append( List._stack[ List._pos ] )
            last = List._stack[ List._pos ]

        elif dep < last._depth :
            for k in List._stack.keys() :
                if k > dep :
                    del List._stack[ k ]
            
            List._pos = dep
            last = List._stack[ List._pos ]
            
            
        # plain adding to this list!
        last._content.append( content )
    # end def
        
    def generate_pre( self, stream, emit, line ) :
        if emit[ 0 ] is not None :
            stream.write( unicode( emit[ 0 ]() ) )
    # end def
    
    def generate_post( self, stream, emit, line ) :
        if emit[ 1 ] is not None :
            stream.write( unicode( emit[ 1 ]() ) )
    # end def
# end class

class ListItem( OrgModeContent ) :
    def __init__( self, line, depth = 0 ) :
        OrgModeContent.__init__( self, line )
        self._depth = depth
    # end def

    def __str__( self ) :
        return transform( "%{Cyan:%s:%}@%s %s <TODO> %{yellow:%s%}" ) % \
            ( OrgModeContent.__str__( self )
            , self._depth
            , self._line
            , self._styles )
    # end def

    def generate_pre( self, stream, emit, line ) :
        if emit is not None:
            line = line[ self._depth+1: ]
            stream.write( unicode( emit( line, self._depth ) ) )
    # end def

# end class


#==============================================================================
# ORG-MODE OPTION
#==============================================================================

class Option( OrgModeContent ) :
    regex = re.compile( "#+" )
    
    def __init__( self, line = None, style = False ) :
        OrgModeContent.__init__( self, line, style )
    # end def
    
    def __str__( self ) :
        return transform( "%{cyan:%s%} %s %{yellow:%s%}" ) % \
            ( OrgModeContent.__str__( self )
            , self._line
            , self._styles
            )
    # end def


# end class

class Mark( Option ) :
    regex = re.compile( "(?<=#\+).*?(?=:)" )
    
    def __init__( self, line ) :
        Option.__init__( self, line )
    # end def
# end class

# #+MARK{:,_BLOCK {OPTION}}

class Block( Option ) :
    regex = re.compile( "(?<=#\+)(begin)|(end)(?=_)" )
    
    blocks = set()
    
    def __init__( self ) :
        Option.__init__( self )
        
        Block.blocks.add( self.__class__ )
    # end def

    def __str__( self ) :
        return transform( "%{cyan:%s%}" ) % \
            ( OrgModeContent.__str__( self )
            )
    # end def
    
    def append( self, content ) :
        assert( isinstance( content, BlockLine ) )
        self._content.append( content )
    # end def
        
    def generate_pre( self, stream, emit, line ) :
        if emit[ 0 ] is not None :
            stream.write( unicode( emit[ 0 ]() ) )
    # end def
    
    def generate_post( self, stream, emit, line ) :
        if emit[ 1 ] is not None :
            stream.write( unicode( emit[ 1 ]() ) )
    # end def
# end class

class BlockLine( OrgModeContent ) :
    def __init__( self, line ) :
        OrgModeContent.__init__( self, line, False )
    # end def
        
    def __str__( self ) :
        return transform( "%{green:%s:%} %s" ) % \
            ( OrgModeContent.__str__( self )
            , self._line 
            )
    # end def
    
    def generate_pre( self, stream, emit, line ) :
        if emit is not None:
            stream.write( unicode( emit( line ) ) )
    # end def

# end class

class Html( Block ) :
    regex = re.compile( "html" )
    
    def __init__( self ) :
        Block.__init__( self )
    # end def
# end class

class Source( Block ) :
    regex = re.compile( "src" )
    
    def __init__( self, language = None ) :
        Block.__init__( self )
    # end def
# end class



#==============================================================================
# ORG-PY
#==============================================================================

from HTML  import HTML
from LATEX import LATEX

class libOrg :
    def __init__( self, filename, configuration = ORG_MODE ) :
        
        self._filename = filename;
        self._content = OrgModeContent( None )
        self._file = []
        
        self._option = \
        { "title" : None
        #, "user"  : {}
        #, "alias" : {}
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
        block = None
        
        for line in orgfile.readlines() :
            self._file.append( line )

            line = ignore.sub( "", line )
            
            if block is not None :
                for j in Block.regex.finditer( line ) :
                    mark = line[ j.span()[0] : j.span()[1] ]
                
                    line = line[ (j.span()[1]+1) : ]
                
                    printf( "%{red:%s -> %s%} %s\n", line, j.span(), mark, 
                            stream = log_file )
                    
                    if mark == "end" :
                        #self._option[ mark ] = Title( line )
                        printf( "end '%s'\n" % line, stream = log_file )
                        
                        if line == "html" :
                            block = None
                            break

                        if line == "src" :
                            block = None
                            break
                    break
                
                if block is None :
                    continue
                
                block.append( BlockLine( line ) )
                continue
            
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
                brk = False
                
                for j in Block.regex.finditer( line ) :
                    mark = line[ j.span()[0] : j.span()[1] ]
                    
                    line = line[ (j.span()[1]+1) : ]
                        
                    printf( "%{Red:%s -> %s%} %s\n", line, j.span(), mark, 
                            stream = log_file )
                    
                    if mark == "begin" and block is None :
                        printf( "begin '%s'\n" % line, stream = log_file )
                        
                        if line == "html" :
                            block = Html()
                            stack[-1].append( block )
                            brk = True
                            break
                        
                        if line.startswith( "src" ) :
                            block = Source()
                            stack[-1].append( block )
                            brk = True
                            break
                    break
                
                if brk :
                    break
                
                for j in Mark.regex.finditer( line ) :
                    mark = line[ j.span()[0] : j.span()[1] ]
                    
                    line = line[ (j.span()[1]+1) : ]
                    
                    printf( "%{Cyan:%s -> %s%} %s\n", line, j.span(), mark, 
                            stream = log_file )
                    
                    if mark == "title" :
                        stack[-1].pop()
                        stack[-1].append( Option( line, True ) )
                        
                        self._option[ mark ] = Title( line )
                        printf( "setting new title '%s'\n" % line, stream = log_file )
                        break
                    
                    # if mark == "help" :
                    #     self._option[ mark ] = line
                    #     printf( "setting new help '%s'\n" % line, stream = log_file )
                    #     break
                    
                    if mark == "user" :
                        split = line.split(":")
                        self._option[ mark ][ split[0] ] = split[ 1:]
                        printf( "adding new user '%s'\n" % line, stream = log_file )
                        break
                    
                    if mark == "alias" :
                        split = line.split(":")
                        self._option[ mark ][ split[0] ] = split[1]
                        printf( "adding new alias '%s'\n" % line, stream = log_file )
                        break
                    
                    self._option[ mark ] = line
                    
                    printf( ">>>>>>>%{Red:'%s'%} '%s'\n"
                            , mark, line, stream = log_file )
                    
                    break
                break
            
            if not text :
                continue
            
            for i in List.regex.finditer( line ) :
                text = False
                last = stack[-1].peek()
                if last is None \
                or not isinstance( last, List ) :
                    _l = List( 0 )
                    stack[-1].append( _l )
                    List._stack = { 0 : _l }
                    List._pos = 0
                
                stack[-1].peek().append( ListItem( line ) )
                printf( "%{yellow:%s%}\n", i.span(), stream = log_file )
                printf( "%{Yellow:%s%}\n"
                      , line[ i.span()[0] : i.span()[1] ].split("|")
                      , stream = log_file )
                printf( "%s\n", List, stream = log_file )
                
                if not text :
                    break

            for i in Table.regex.finditer( line ) :
                text = False
                last = stack[-1].peek()
                if last is None \
                or not isinstance( last, Table ) :
                    _l = Table()
                    stack[-1].append( _l )
                
                stack[-1].peek().append( TableRow( line ) )
                printf( "%{Red:%s%}\n", i.span(), stream = log_file )
                printf( "%{Red:%s%}\n"
                      , line[ i.span()[0] : i.span()[1] ].split("|")
                      , stream = log_file )
                printf( "%s\n", Table, stream = log_file )
                
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
        
        self._content.generate( stream, emit, self )
        
        if  "epilog" in emit \
        and emit[ "epilog" ] is not None :
            stream.write( unicode( emit[ "epilog" ] ) )
        
        #print stream
    # end def
    
    def generate_object( self, obj, emit = HTML ) :
        stream = io.StringIO()
        obj.generate( stream, emit, self )
        return stream.getvalue()
    # end def
    
    def get_option( self, option ) :
        if option in self._option :
            return self._option[ option ]
        else :
            return None
    # end def

    def findFirstTable( self, obj = None ) :
        if obj is None : #isinstance( self, libOrg.libOrg ) :
            return self.findFirstTable( self._content )
        #if isinstance( obj, libOrg.OrgModeContent ) :
        if isinstance( obj, OrgModeContent ) :
            for c in obj._content :
                #if isinstance( c, libOrg.Table ) :
                if isinstance( c, Table ) :
                    return c
        else :
            assert "invalid 'org' object to analyze"
        return None
    # end def
    
    # generic function can be moved to 'liborg' repository!
    def iterateTable( self, obj, row_action = lambda y, row : True, cell_action = lambda x, y, cell : None ) :
        def print_row( y, row ) :
            print y, row
            return True
        # end def
        def print_cell( x, y, row ) :
            print x, y, row        
        # end def
        if row_action is None :
            row_action = print_row
        if cell_action is None :
            cell_action = print_cell
        
        #assert isinstance( obj, libOrg.Table )    
        assert isinstance( obj, Table )    
        y = 0
        for row in obj._content :
            #assert isinstance( row, libOrg.TableRow )
            assert isinstance( row, TableRow )
            result = row_action( y, row )
            if result == True or result is None :
                x = 0
                for cell in row._content :
                    #assert isinstance( cell, libOrg.TableCell )
                    assert isinstance( cell, TableCell )
                    cell_action( x, y, cell )
                    x = x + 1
            y = y + 1
    # end def
# end class



if __name__ == "__main__" :
    
    if len(sys.argv) != 2 :
        print "usage: python libOrg.py <ORG-FILE>"
        sys.exit(-1)
        
    file_name = sys.argv[1]    
    
    orgpy = libOrg( file_name )
    
    print "DUMPING"
    orgpy.dump()
    
    print "EMITING CODE"
    
    with io.open( file_name + ".html" , "w" ) as fd:
        orgpy.generate( fd )
        orgpy.generate( sys.stdout )
        
    with io.open( file_name + ".tex" , "w" ) as fd:
        orgpy.generate( fd, emit=LATEX )
        orgpy.generate( sys.stdout, emit=LATEX )
        
    print orgpy._option
