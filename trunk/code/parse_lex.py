import ply.lex as lex

# List of tokens
tokens = (
  'COLON',
  'COMMA',
  'DIRECT',
  'NEWLINE',
  'NOTE',
  'NUMB'
)

def t_COLON(tok):
  r':'
  return tok

def t_COMMA(tok):
  r','
  return tok

def t_DIRECT(tok):
  r'\..*'
  return tok

def t_NEWLINE(tok):
  r'\n+'
  tok.lexer.lineno += tok.value.count('\n')
  return tok

def t_NOTE(tok):
  r'\#.*'
  tok.value = tok.value[1:]
  return tok

def t_hex(tok):
  r'0x([0-9a-fA-F]{8}|[0-9a-fA-F]{4})'
  tok.type = 'NUMB'
  return tok

def t_offset(tok):
  r'[0-9]+\([a-zA-Z0-9$_.]+\)'
  tok.type = 'NUMB'
  return tok

def t_dec(tok):
  r'-?[0-9]+'
  tok.type = 'NUMB'
  return tok

def t_NUMB(tok):
  r'[a-zA-Z0-9$_.+()-]+'
  return tok

# Don't use tabs and spaces
t_ignore = ' \t'

def t_error(tok):
  print('Illegal character "%s"' % tok.value[0])
  tok.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
