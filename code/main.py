#!/usr/bin/python
from parse_yacc import parse
from optimize import optimize
from peep import createAssemblyCode
import sys

if __name__ == '__main__':
<<<<<<< .mine
    lengte = len(sys.argv)
    if lengte < 2:
      print 'Run: python %s assembly.s' % sys.argv[0]
      sys.exit(1) 

    # Parsing and optimization
    parsed = parse(sys.argv[1])
    new = optimize(parsed, var=1)

    if lengte > 2:
=======

  if len(sys.argv) < 2:
    print 'Run: python %s benchmarks/assembly.s' % sys.argv[0]
    sys.exit(1)    
  # Parsing and optimization
  parsed = parse(sys.argv[1])
  new = optimize(parsed, var=1)
  try:
    if len(sys.argv) > 2:
>>>>>>> .r70
      file_func = open(sys.argv[2], 'w+')
<<<<<<< .mine
      f.write(createAssemblyCode(new))
      f.close()
=======
      file_func.write(createAssemblyCode(new))
      file_func.close()
  except:      
    file_func.close()
    sys.exit(1)
>>>>>>> .r70
<<<<<<< .mine



=======
>>>>>>> .r70
