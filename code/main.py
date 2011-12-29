#!/usr/bin/python
import sys
from optparse import OptionParser

from parser import parse
from optimize import optimize

if __name__ == '__main__':
  usage = "usage: %prog [options] file"
  parser = OptionParser(usage)
  parser.add_option('-i', '--input', dest='input', help='Input the assembly file',
                          metavar='FILE')
  parser.add_option('-d', '--dest', dest='filename', help='Destination of ' \
                          'optimized assembly file',
                          metavar='FILE')
  (options, args) = parser.parse_args()
  if len(args) != 1:
    parser.error("incorrect number of arguments")

  # Controlling input of assembly file
  if options.input == None:
    parser.error('Missing assembly file argument')
  if options.filename == None:
    output = options.filename[0] + '_opt'
  else:
    output = options.filename[0] + '_opt.' + options.filename[1]
  
  # Controlling opening input and output files
  try:
    in_file = open(options.input, 'r')
  except:
    sys.exit('Not able to open input file: ' + options.input)
  try:
    out_file = open(output, 'w')
  except:
    in_file.close()
    sys.exit('Not able to make output file' + output) 

  # Parse and optimization
  parsing = parser.parse(in_file.readlines())
  optimized = optimize(parsing)
  in_file.close()

  out = write_statements(optimized)
  out_file.write(out)
  out_file.close()

if __name__ == '__main__'
  main()
