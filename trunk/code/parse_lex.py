import ply.lex as lex

# Tokens list
tokens = (
  'COLON',
  'COMMA',
  'COMMENT',
  'DIRECTIVE',
  'NEWLINE',
  'WORD'
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

def t_NEWLINE(t):
  r'\n+'
  t.lexer.lineno += t.value.count('\n')
  return tok

def t_hex_word(t):
  r'0x([0-9a-fA-F]{8}|[0-9a-fA-F]{4})'
  t.type = 'WORD'
  return tok

def t_offset_address(t):
  r'[0-9]+\([a-zA-Z0-9$_.]+\)'
  t.type = 'WORD'
  return tok

def t_int(t):
  r'-?[0-9]+'
  t.type = 'WORD'
  return tok

def t_WORD(t):
  r'[a-zA-Z0-9$_.+()-]+'
  return tok

#def t_DECI(tok):
#  r'[0-9]+'
#  return tok

#def t_HEXI(tok):
#  r'0x[0-9]{8}'
#  return tok

#def t_OFFSET(tok):
#  r'[0-9]+\([a-zA-Z0-9$_.]+\)'
#  return tok

# Handle errors
def t_error(tok):
  print("Illegal token '%s'" % tok.value[0])
  t.lexer.skip(1)

# '[ \t\n]' ' \t\n'
t_ignore  = ' \t'

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
