import ply.lex as lex

tokens = (
  'COMMA',
  'COMMENT', 
  'COLON',
  'DIRECTIVE',
  'NEWLINE', 
  'WORD'
)

# Tokens
def t_COMMA(tok):
    r','
    return tok

def t_COMMENT(tok):
    r'\#.*'
    tok.value = tok.value[1:]
    return tok

def t_COLON(tok):
    r':'
    return tok

def t_DIRECTIVE(tok):
    r'\..*'
    return tok

def t_NEWLINE(tok):
    r'\n+'
    tok.lexer.lineno += tok.value.count('\n')
    return tok

def t_hex(tok):
    r'0x([0-9a-fA-F]{8}|[0-9a-fA-F]{4})'
    tok.type = 'WORD'
    return tok

def t_offset(tok):
    r'[0-9]+\([a-zA-Z0-9$_.]+\)'
    tok.type = 'WORD'
    return tok

def t_dec(tok):
    r'-?[0-9]+'
    tok.type = 'WORD'
    return tok

def t_WORD(tok):
    r'[a-zA-Z0-9$_.+()-]+'
    return tok

t_ignore = ' \t'

def t_error(tok):
    print('Illegal character "%s"' % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
