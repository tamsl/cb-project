import ply.yacc as yacc
from parse_lex import tokens
from peep import Expression

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
  expr.append(Expression('comment', p[1]))

def p_instruction(p):
  '''
  list : instruction
  '''
  pass

def p_directive(p):
  '''
  instruction : DIRECTIVE
  '''
  expr.append(Expression('directive', p[1]))

def p_instr_command(p):
  '''
  instruction : command
  '''
  pass

def p_command(p):
  '''
  command : 
  | argument argument argument 
  | argument argument 
  | argument 
  '''
  expr.append(Expression('command', p[1]))

def p_argument(p):
  '''
  argument : 
  | OFFSET
  | DECI 
  | HEXI
  '''
  expr.append(Expression('label', p[1]))

def p_error(p):
  pass

# Build the parser
parser = yacc.yacc() 

def parse(p):
  expr = []
  try:
    to_parse = open(p).read()
    yacc.parse(to_parse)
  except IOError:
    raise Exception('Wrong file "%s"' % p)
  parsed = parser.parse(to_parse)
  print parsed

  return Block(expr)
