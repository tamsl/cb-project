import ply.yacc as yacc
import ply.lex as lex

# hier hoort nog wat van tok

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

def t_space(tok):
  r'\s+'
  return tok

def t_line(tok):
  '\l+'
  return tok

def t_error(tok):
  print("Wrong character '%s'" % tok.value[0])
  t.lexer.skip(1)

lexer = lex.lex()

parse_rules = 'system'

def p_system
  '''system : system list '''
  pass

parser = yacc.yacc() 


