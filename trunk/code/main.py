#!/usr/bin/python
import sys
from optparse import OptionParser

from parser import parse
from optimize import optimize

if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-i', '--input', dest='input', help='Input the assembly file',
                          metavar='FILE')
  parser.add_option('-o', '--output', dest='output', help='Output destination of ' \
                          'optimized assembly file',
  (options, args) = parser.parse_args()
  
  # Controlling input of assembly file
  input_file = options.input
  if input_file == None:
    parser.error('Missing assembly file argument')
  output_file = options.output
  if output_file == None:
    output_file = input_file.split('/')[-1].rsplit('.', 1)
    if (len(output_file) < 1):
      output_file = output_file[0] + '_opt'
    else:
      output_file = output_file[0] + '_opt.' + output_file[1] 

  # Controlling opening input and output files
  try:
    in_file = open(input_file, 'r')
  except:
    sys.exit('Not able to open input file: ' + input_file)
  try:
    out_file = open(output_file, 'w')
  except:
    in_file.close()
    sys.exit('Not able to make output file' + output_file) 

  # Parse and optimization
  parsing = parser.parse(in_file.readlines())
  optimized = optimize(parsing)

  out = write_statements(optimized)
  out_file.write(out)

  in_file.close()
  out_file.close()
  print( output_file + ': Destination output file')

if __name__ == '__main__'
  main()
