import ply.yacc as yacc

precedence = 'system'

def p_system(p):
  '''
  system : list
  '''
  pass

def p_comment(p):
  '''
  list : COMMENT
  '''

def p_instruction(p):
  '''
  list : instruction
  '''
  pass

def p_directive(p):
  '''
  instruction : DIRECTIVE
  '''

def p_instr_command(p):
  'instruction : command'
  pass

def p_command(p):
  '''
  command : 
  | argument argument argument argument 
  | argument argument argument 
  | argument argument 
  | argument 
  '''

def p_argument(p):
  '''
  argument : REGISTER | OFFSET | DECI | HEXI
  '''

def p_error(p):
  pass

# Build the parser
parser = yacc.yacc() 

def parse(p):
  try:
    to_parse = open(p).read()
    yacc.parse(to_parse)
  except IOError:
    raise Exception('Wrong file "%s"' % p)
  parsed = parser.parse(to_parse)
  return parsed
