#!/usr/bin/python
import sys
from optparse import OptionParser

import parse_yacc
import optimize

def main():
  usage = "usage: %prog [options] file"
  parser = OptionParser(usage)
  parser.add_option("-i", "--input", dest="input", help="Input the assembly file",
                          metavar="FILE")
  parser.add_option("-d", "--dest", dest="filename", help="Destination of " \
                          "optimized assembly file",
                          metavar="FILE")
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()
  (options, args) = parser.parse_args()


  # Controlling opening input and output files
  try:
    in_file = open(options.input, "r")
  except:
    sys.exit("Not able to open input file: " + options.input)
  # Parse and optimization
  parsing = parse_yacc.parse(in_file.readlines())
  optimized = optimize.optimizer(parsing)
  in_file.close()

  # Controlling input of assembly file
  if options.input == None:
    parser.error("Missing assembly file argument")
  if options.filename == None:
    inp = options.input
    out = options.filename
    out = inp.split('/')[-1].rsplit('.', 1)
    if (len(out) > 1):
      output = out[0] + '_opt.' + out[1]
    else:
      output = out[0] + '_opt'
  
  try:
    out_file = open(output, 'w')
  except:
    in_file.close()
    sys.exit("Not able to make output file: " + output) 

  out = createAssemblyCode(optimized)
  out_file.write(out)
  out_file.close()

if __name__ == '__main__':
  main()
