#!/usr/bin/python
from parse_yacc import parse
from optimize import optimizer
from peep import createAssemblyCode
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python %s FILE' % argv[0]
        sys.exit(1)

    # Parse File
    original = parse(sys.argv[1])
    optimized = optimizer(original, verbose=1)

    if len(sys.argv) > 2:
        # Save output assembly
        output = createAssemblyCode(optimized)
        f = open(sys.argv[2], 'w+')
        f.write(out)
        f.close()
