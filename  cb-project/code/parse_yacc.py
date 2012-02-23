import ply.yacc as yacc
from parse_lex import tokens
from peep import Expression as S, Block

# List with expressions
expressions = []

# Parsing rules
begin = 'system'

def p_input(p):
  '''
  system :
         | system list
  '''
  pass

def p_list_instr(p):
  '''
  list : instr NEWLINE
  '''
  pass

def p_note(p):
  '''
  list : NOTE NEWLINE
  '''
  expressions.append(S('note', p[1], inline=False))

def p_note_newline(p):
  '''
  list : instr NOTE NEWLINE
  '''
  expressions.append(S('note', p[2], inline=True))

def p_inst_command(p):
  '''
  instr : control
  '''
  pass

def p_direct(p):
  '''
  instr : DIRECT
  '''
  expressions.append(S('direct', p[1]))

def p_numb_colon(p):
  '''
  instr : NUMB COLON
  '''
  expressions.append(S('label', p[1]))

def p_control(p):
  '''
  control : 
          | NUMB NUMB COMMA NUMB COMMA NUMB
          | NUMB NUMB COMMA NUMB
          | NUMB NUMB
          | NUMB
  '''
  expressions.append(S('control', p[1], *list(p)[2::2]))

def p_error(p):
  print 'Error in the parser.'

# Build the parser
yacc.yacc()

# Open an assembly file and parse it
def parse(p):
  global expressions
  expressions = []

  try:
    to_parse = open(p).read()
    yacc.parse(to_parse)
  except IOError:
    raise Exception('File "%s" could not be opened' % p)

  return Block(expressions)
