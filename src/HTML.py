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

, "Source"        : ( ( lambda : "<pre>\n" )
                    , ( lambda : "</pre>\n" )
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
