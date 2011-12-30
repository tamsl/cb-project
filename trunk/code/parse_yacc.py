import ply.yacc as yacc
from parse_lex import tokens
from peep import Expression, Block

expressions = []

beginning = 'system'

def p_system(p):
  '''
  system : list
  '''
  pass

def p_comment(p):
  '''
  list : COMMENT NEWLINE
  '''
  expressions.append(Expression('comment', p[1], inline=False))

def p_instruction_comment(p):
  '''
  list : instruction COMMENT NEWLINE
  '''
  expressions.append(S('comment', p[2], inline=True))

def p_instruction(p):
  '''
  list : instruction NEWLINE
  '''
  pass

def p_instr_command(p):
  '''
  instruction : command
  '''
  pass

def p_directive(p):
  '''
  instruction : DIRECTIVE
  '''
  expressions.append(Expression('directive', p[1]))

def p_label(p):
  '''
  instruction : WORD COLON
  '''
  expressions.append(Expression('label', p[1]))

def p_command(p):
  '''
  command : WORD WORD COMMA WORD COMMA WORD
          | WORD WORD COMMA WORD
          | WORD WORD
          | WORD
  '''
  expressions.append(Expression('command', p[1], *list(p)[2::2]))

def p_error(p):
  pass

# Build the parser
parser = yacc.yacc() 

def parse(p):
  global expressions
  expressions = []

  try:
    to_parse = open(p).read()
    yacc.parse(to_parse)
  except IOError:
    raise Exception('Wrong file "%s"' % p)
  parsed = parser.parse(to_parse)
  print parsed

  return Block(expressions)
