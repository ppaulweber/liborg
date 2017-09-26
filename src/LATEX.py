#
#   Copyright (c) 2014-2017 Philipp Paulweber
#   All rights reserved.
#
#   Developed by: Philipp Paulweber
#                 https://github.com/ppaulweber/liborg
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

seperator = False

def table_row_cell( kind, text, isLast = None ) :
    global seperator
    if kind == "TableRow" :
        if text == True :
            seperator = False
            return ""
        else :
            if not seperator :
                return "\\\\\n"
            else :
                return ""
        
    elif kind == "TableCell" :
        if text == "" :
            return " & "
        elif text is not None and not isLast :
            return "%s & " % text
        elif text is not None and isLast :
            return "%s " % text
        else :
            if not seperator :
                seperator = True
                return "\\hline\n"
            else :
                return ""
        
    else :
        assert( 0 )
# end


LATEX = \
{ "comment"       : ( lambda text : "%%%% %s\n" % text )

, "prolog"        : """%% prolog
\\documentclass{article}
\\usepackage{hyperref}
\\begin{document}
"""

, "epilog"        : """%% epilog
\\end{document}
"""

, "dependency"    : "\n"
                    "%% list here more dependencies"

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

, "BlockLine"     : ( lambda line : "%s\n" % line )

, "Html"          : ( ( lambda : "%% begin html\n" )
                    , ( lambda : "%% end   html\n" )
                    )

, "Source"        : ( ( lambda : "%% begin src\n" )
                    , ( lambda : "%% end   src\n" )
                    )

, "Bold"          : ( ( lambda text : "\\textbf{" )
                    , ( lambda text : "}" )
                    )

, "Italic"        : ( ( lambda text : "\\textit{" )
                    , ( lambda text : "}" )
                    )

, "Code"          : ( ( lambda text : '\\texttt{' )
                    , ( lambda text : '}' )
                    )

, "List"          : ( ( lambda : '\\begin{itemize}\n' )
                    , ( lambda : '\\end{itemize}\n' )
                    )

, "ListItem"      : ( lambda text, depth : '\\item %s\n' % text )

  
, "Table"         : ( ( lambda columns : '\\begin{table}[h!]\n\\begin{tabular}{%s}\n' % \
                        "|".join([ "l" ] * columns)
                      )
                    , ( lambda         : '\\end{tabular}\n\\end{table}\n' )
                    )

, "TableRow"      : ( ( lambda : table_row_cell( "TableRow", True  ) )
                    , ( lambda : table_row_cell( "TableRow", False ) )
                    )

, "TableCell"     : ( lambda text, isLast : table_row_cell( "TableCell", text, isLast ) )

, "Link"          : ( ( lambda link : '\\href{%s}{%s}' % \
                        ( link["link"]
                        , link["name"]
                        ) 
                      )
                    , None
                    )

#, "Rule"          : ( ( lambda text : '<hr>' )
#                    , None
#                    )

# , "Footnote"      : ( ( lambda text : '<sup><a href="%s">%s</a></sup>' % \
#                         ( re.search( ".*?(?=:)" ,   text[4:] ).group(0)
#                         , re.search( "(?<=:).*?(?=\])", text[4:] ).group(0)
#                         ) 
#                       )
#                     , None
#                     )

# , "Input"         : ( ( lambda inp : '<input type="%s" name="%s" value="%s" />' % \
#                         ( inp[ "type" ]
#                         , inp[ "name" ]
#                         , inp[ "value" ]
#                         )
#                       )
#                     , None
#                     )

, "Data"          : ( ( lambda data : 
                        data[ "error" ] if data[ "error" ] is not None else
                        data[ "value" ]
                      )
                    , None
                    )
}
