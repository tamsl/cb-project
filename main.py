#!/usr/bin/python
from code.parse_yacc import parse_file
from code.optimize import optimize
from code.peep import createAssemblyCode

if __name__ == '__main__':
    from sys import argv, exit

    if len(argv) < 2:
        print 'Usage: python %s FILE' % argv[0]
        exit(1)

    # Parse File
    original = parse_file(argv[1])
    optimized = optimize(original, verbose=1)

    if len(argv) > 2:
        # Save output assembly
        out = write_statements(optimized)
        f = open(argv[2], 'w+')
        f.write(out)
        f.close()