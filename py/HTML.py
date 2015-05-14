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

, "BlockLine"     : ( lambda line : "%s\n" % line )

, "Html"          : ( ( lambda : "<!-- begin html -->\n" )
                    , ( lambda : "<!--  end  html -->\n" )
                    )

, "Source"        : ( ( lambda : "<!-- begin src -->\n" )
                    , ( lambda : "<!--  end  src -->\n" )
                    )

, "Bold"          : ( ( lambda text : "<b>" )
                    , ( lambda text : "</b>" )
                    )

, "Italic"        : ( ( lambda text : "<i>" )
                    , ( lambda text : "</i>" )
                    )

, "Code"          : ( ( lambda text : '<code>' )
                    , ( lambda text : '</code>' )
                    )

, "List"          : ( ( lambda : '<ul>\n' )
                    , ( lambda : '</ul>\n' )
                    )

, "ListItem"      : ( lambda text, depth : '<li>%s</li>\n' % text )

, "Table"         : ( ( lambda columns : '<table>\n' )
                    , ( lambda         : '</table>\n' )
                    )

, "TableRow"      : ( ( lambda : '<tr>' )
                    , ( lambda : '</tr>\n' )
                    )

, "TableCell"     : ( lambda text, isLast : '<td>&nbsp;</td>' if text == "" else 
                      '<td>%s</td>' % text                    if text is not None else 
                      '<td><hr></td>' 
                    )
  
, "Link"          : ( ( lambda link : '<a href="%s">%s</a>' % \
                        ( link["link"]
                        , link["name"]
                        ) 
                      )
                    , None
                    )

#, "Rule"          : ( ( lambda text : '<hr>' )
#                    , None
#                    )

, "Footnote"      : ( ( lambda text : '<sup><a href="%s">%s</a></sup>' % \
                        ( re.search( ".*?(?=:)" ,   text[4:] ).group(0)
                        , re.search( "(?<=:).*?(?=\])", text[4:] ).group(0)
                        ) 
                      )
                    , None
                    )

, "Input"         : ( ( lambda inp : '<input type="%s" name="%s" value="%s" />' % \
                        ( inp[ "type" ]
                        , inp[ "name" ]
                        , inp[ "value" ]
                        )
                      )
                    , None
                    )

, "Data"          : ( ( lambda data : 
                        data[ "error" ] if data[ "error" ] is not None else
                        data[ "value" ]
                      )
                    , None
                    )

}
