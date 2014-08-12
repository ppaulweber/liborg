# 
# Copyright (c) 2014 Philipp Paulweber
# 
# This file is part of the 'liborgpy' project which is released under a NCSA
# open source software license. For more information, see the LICENSE.txt 
# file in the project root directory.
#

from OrgPy import OrgPy, LATEX

import sys
import io

if __name__ == "__main__" :
    
    if len(sys.argv) != 2 :
        print "usage: python main.py <ORG-FILE>"
        sys.exit(-1)

    file_name = sys.argv[1]    
    
    orgpy = OrgPy( file_name )
    
    print "DUMPING"
    orgpy.dump()
    
    print "EMITING CODE"
    
    file_name = ".attic/out"
    
    with io.open( file_name + ".html" , "w" ) as fd:
        orgpy.generate( fd )
        orgpy.generate( sys.stdout )
        
    with io.open( file_name + ".tex" , "w" ) as fd:
        orgpy.generate( fd, emit=LATEX )
    
