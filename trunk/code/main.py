#!/usr/bin/python
from parse_yacc import parse_file
from optimize import optimize
from peep import createAssemblyCode
import sys

if __name__ == '__main__':
  try:
    if len(sys.argv) < 2:
      print 'Usage: python %s FILE' % sys.argv[0]
  except:
    sys.exit(1)    
  # Parsing and optimization
  original = parse_file(sys.argv[1])
  optimized = optimize(original, verbose=1)
  try:
    if len(sys.argv) > 2:
      file_func = open(sys.argv[2], 'w+')
  except:      
    file_func.close()
    sys.exit(1)

    file_func.write(createAssemblyCode(optimized))
    file_func.close()

