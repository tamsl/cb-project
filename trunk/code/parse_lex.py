import ply.lex as lex

# Tokens list
tokens = (
  'COLON',
  'COMMA',
  'COMMENT',
  'DIRECTIVE',
  'DECI',
  'HEXI',
  'OFFSET'
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

# Handle errors
def t_error(tok):
  print("Illegal token '%s'" % tok.value[0])
  t.lexer.skip(1)

# '[ \t\n]'
t_ignore  = ' \t\n'

# Build the lexer
lexer = lex.lex()

# Input for the lexer
#lexer.input(data)

# Tokenize
#while True:
#  tok = lexer.token()
#  if not tok:
#    break      # No more input
#  print tok
