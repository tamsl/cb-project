import ply.yacc as yacc
import ply.lex as lex

# Tokens list
tokens = (
  'COLON',
  'COMMA',
  'COMMENT',
  'DIRECTIVE',
  'DECI',
  'HEXI',
  'OFFSET',
  'REGISTER'
)

def t_COLON(tok):
  r':'
  return tok

def t_COMMA(tok):
  r','
  return tok

def t_COMMENT(tok):
  r'\#.+'
  return tok

def t_DIRECTIVE(tok):
  r'\..+'
  return tok

def t_DECI(tok):
  r'[0-9]+'
  return tok

def t_HEXI(tok):
  r'0x[0-9]{8}'
  return tok

def t_OFFSET(tok):
  r'[0-9]+\([a-zA-Z0-9$_.]+\)'
  return tok

def t_REGISTER(tok):
  r'\$[a-zA-Z0-9]+'
  return tok

# Handle errors
def t_error(tok):
  print("Illegal token '%s'" % tok.value[0])
  t.lexer.skip(1)

# '[ \t\n]'
t_ignore  = ' \t\n'

# Build the lexer
lexer = lex.lex()

while 1:
  tok = lexer.token()
  if not tok:
    break

precedence = 'system'

def p_system(p):
  '''
  system : 
  | instruction
  | command_comment
  | command
  | directive
  | comment
  '''
  pass

def p_instruction_command(p):
    '''
    instruction : command
    '''
    pass

def p_command_comment(p):
  '''
  command_comment : command COMMENT
  '''
  p[0] = p[1]

def p_command(p):
  '''
  command : 
  | argument argument argument argument 
  | argument argument argument 
  | argument argument 
  | argument 
  '''
  p[0] = (p.slice[1].type, p[1])

def p_argument(p):
  '''
  argument : REGISTER | OFFSET | DECI | HEXI
  '''
  p[0] = (p.slice[1].type, p[1])

def p_directive(p):
  '''
  directive : DIRECTIVE
  '''
  p[0] = (p.slice[1].type, p[1])

def p_comment(p):
  '''
  comment : COMMENT
  '''
  pass

def p_error(p):
  pass

# Build the parser
parser = yacc.yacc() 

while 1:
  try:
    s = raw_input()
  except EOFError:
    break
  if not s:
    continue
  parsed = parser.parse(s)
