# 
# Copyright (c) 2014 Philipp Paulweber
# 
# This file is part of the 'liborgpy' project which is released under a NCSA
# open source software license. For more information, see the LICENSE.txt 
# file in the project root directory.
#

from OrgPy import *


if __name__ == "__main__" :
    
    if len(sys.argv) != 2 :
        print "usage: python main.py <ORG-FILE>"
        sys.exit(-1)

    OrgPy( sys.argv[1] )
