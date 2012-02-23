#!/usr/bin/python
from parse_yacc import parse
from optimize import optimize
from peep import createAssemblyCode
import sys

if __name__ == '__main__':

  if len(sys.argv) < 2:
    print 'Run: python %s benchmarks/assembly.s output.s' % sys.argv[0]
    exit(1)    
  # Parsing and optimization
  parsed = parse(sys.argv[1])
  new = optimize(parsed, var=1)

  if len(sys.argv) > 2:
    # Save output assembly
    file_func = open(sys.argv[2], 'w+')
    file_func.write(createAssemblyCode(new))
    file_func.close()
