#!/usr/bin/python
from parse_yacc import parse
from optimize import optimize
from peep import createAssemblyCode
import sys

if __name__ == '__main__':
  try:
    if len(sys.argv) < 2:
      print 'Run: python %s assembly.s' % sys.argv[0]
  except:
    sys.exit(1)    
  # Parsing and optimization
  parsed = parse(sys.argv[1])
  new = optimize(parsed, var=1)
  try:
    if len(sys.argv) > 2:
      file_func = open(sys.argv[2], 'w+')
  except:      
    file_func.close()
    sys.exit(1)

    file_func.write(createAssemblyCode(new))
    file_func.close()

