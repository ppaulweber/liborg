#   
#   Copyright (c) 2015 Philipp Paulweber
#   All rights reserved.
#   
#   Developed by: Philipp Paulweber
#                 https://github.com/ppaulweber/liborg
#   
#   Permission is hereby granted, free of charge, to any person obtaining a 
#   copy of this software and associated documentation files (the "Software"), 
#   to deal with the Software without restriction, including without limitation 
#   the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#   and/or sell copies of the Software, and to permit persons to whom the 
#   Software is furnished to do so, subject to the following conditions:
#   
#   * Redistributions of source code must retain the above copyright 
#     notice, this list of conditions and the following disclaimers.
#   
#   * Redistributions in binary form must reproduce the above copyright 
#     notice, this list of conditions and the following disclaimers in the 
#     documentation and/or other materials provided with the distribution.
#   
#   * Neither the names of the copyright holders, nor the names of its 
#     contributors may be used to endorse or promote products derived from 
#     this Software without specific prior written permission.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
#   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#   CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
#   WITH THE SOFTWARE.
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
