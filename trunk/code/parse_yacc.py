import ply.yacc as yacc
from parse_lex import tokens
from peep import Expression, Block
import sys
expressions = []
raise_on_error = False
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

error_count = 0
def p_error(p):
  print "Syntax error in input!"
  global raise_on_error
  global error_count
  error_count +=1
  if raise_on_error: raise Exception()

# Build the parser
parser = yacc.yacc() 

def parse(p):
  #  """Parse a given Assembly file, return a Block with Statement objects
  # containing the parsed instructions."""
  #  global statements

   # statements = []

   # try:
   #     content = open(filename).read()
   #     yacc.parse(content)
   # except IOError:
   #     raise Exception('File "%s" could not be opened' % filename)
#
   # return Block(statements) 
  if len(sys.argv) > 1:
    counter = 1
    for line in open(sys.argv[0], 'r').readlines():
      if not line.strip(): continue
      result = parser.parse(line)
      print counter, result
      counter +=1
      #if counter % 50 == 0: raw_input('pres key')
    print 'errors: %d\n' % error_count
    # interactive
  else:
    while True:
     try:
       s = raw_input('asmyacc > ')
     except EOFError:
       break
     if not s: continue
     result = parser.parse(s)
     print repr(result)
